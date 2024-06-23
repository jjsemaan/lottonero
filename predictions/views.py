from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.contrib import messages
from django.db.models import Max
from django.db.models import Q
from django.db.models import Max
from scraping.models import EuroMillionsResult
from .forms import UploadImageForm, OverwriteConfirmationForm
from .models import Prediction, UploadImageModel, ShuffledPrediction
from orders.models import Subscription
from scraping.models import EuroMillionsResult
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
import datetime
import cloudinary.uploader
import os
import tempfile
import random


def admin_required(view_func):
    """
    Decorator to restrict view access to admin users only.
    """
    decorated_view_func = user_passes_test(lambda u: u.is_staff)(view_func)
    return decorated_view_func


@admin_required
def get_image_url(name):
    """
    Retrieves the URL of an image by its name from the UploadImageModel, accessible only to admin users.
    """
    image = UploadImageModel.objects.filter(name=name).values("image").first()
    return image["image"] if image else None


def read_data_from_database(request):
    """
    Fetches and displays all EuroMillions result entries from the database.
    """
    results = EuroMillionsResult.objects.all()
    return render(
        request, "predictions/predictions.html", {"results": results}
    )


@login_required
def display_predictions(request):
    """
    Displays lottery predictions with associated images only to subscribed users.

    This view checks if the user has active subscriptions to certain products necessary for accessing AI predictions.
    If not subscribed, the user is redirected to the pricing page. Otherwise, it retrieves the latest predictions,
    caches and retrieves associated images, and presents these formatted predictions on a web page.

    Args:
        request (HttpRequest): The HttpRequest object containing metadata about the request.

    Returns:
        HttpResponse: Renders a template with predictions and their corresponding images if authorized,
                      or redirects to the pricing page if access is denied.
    """
    if not Subscription.objects.filter(
        Q(
            user=request.user,
            active=True,
            product_name="AI Predictions for EuroMillions Lotto",
        )
        | Q(user=request.user, active=True, product_name="Premium Full Access")
    ).exists():
        messages.error(
            request,
            "Access denied. You are not subscribed to AI Predictions or Premium Full Access.",
        )
        return redirect("pricing_page")

    latest_date = Prediction.objects.aggregate(
        latest_date=Max("prediction_date")
    )["latest_date"]
    predictions = Prediction.objects.filter(prediction_date=latest_date)

    image_cache = {}

    def get_cached_image_url(value):
        if value not in image_cache:
            image_cache[value] = get_image_url(value)
        return image_cache[value]

    predictions_with_images = []
    for prediction in predictions:
        pred_ball_images = [
            get_cached_image_url(f"{getattr(prediction, f'pred_ball_{i}'):02}")
            for i in range(1, 6)
        ]
        pred_lucky_images = [
            get_cached_image_url(
                f"star{getattr(prediction, f'pred_lucky_{i}')}"
            )
            for i in range(1, 3)
        ]

        predictions_with_images.append(
            {
                "prediction": prediction,
                "pred_ball_1_image": pred_ball_images[0],
                "pred_ball_2_image": pred_ball_images[1],
                "pred_ball_3_image": pred_ball_images[2],
                "pred_ball_4_image": pred_ball_images[3],
                "pred_ball_5_image": pred_ball_images[4],
                "pred_lucky_1_image": pred_lucky_images[0],
                "pred_lucky_2_image": pred_lucky_images[1],
            }
        )

    return render(
        request,
        "predictions/predictions.html",
        {"predictions_with_images": predictions_with_images},
    )


@admin_required
def backoffice(request):
    return render(request, "backoffice/backoffice.html")


@admin_required
@csrf_protect
def train_classifier(request):
    """
    Handle POST requests to train a classifier and generate lottery predictions.

    This view function processes a POST request to train a RandomForestClassifier
    using historical EuroMillions lottery results and generates unique lottery
    number predictions. The predictions are stored in the database and appropriate
    templates are rendered based on the result.

    Parameters:
    request (HttpRequest): The HTTP request object containing a POST request with a 'draw_date' field.

    Returns:
    HttpResponse: Renders a template with a success message and new predictions if successful.
                  Renders a template with a message if predictions for the draw date already exist.
                  Returns a 400 Bad Request response if the 'draw_date' is missing or invalid.
                  Returns a 500 Internal Server Error response if any error occurs during processing.

    The function performs the following steps:
    1. Validates the presence and format of 'draw_date' in the POST request.
    2. Checks if predictions for the provided draw date already exist.
    3. If no existing predictions are found:
       a. Retrieves historical EuroMillions results from the database.
       b. Trains two RandomForestClassifier models: one for predicting main balls and another for lucky stars.
       c. Generates unique predictions ensuring no duplicate sets of numbers.
       d. Saves the new predictions to the database.
       e. Renders a template displaying the new predictions.
    4. Handles errors by returning appropriate HTTP responses.
    """

    if request.method == "POST":
        draw_date = request.POST.get("draw_date")

        if not draw_date:
            return HttpResponseBadRequest("Draw date is required.")

        try:
            draw_date_obj = datetime.datetime.strptime(draw_date, "%Y-%m-%d")
            draw_date_str = draw_date_obj.strftime("%Y/%m/%d")
        except ValueError:
            return HttpResponseBadRequest("Invalid date format.")

        # Check if predictions for this draw date already exist
        if Prediction.objects.filter(draw_date=draw_date_str).exists():
            return render(
                request,
                "backoffice/predictions_exist.html",
                {"message": "Predictions for this draw date already exist."},
            )

        try:
            last_scraped_result = EuroMillionsResult.objects.order_by(
                "-draw_date"
            ).first()
            today_str = timezone.now().strftime("%Y/%m/%d")

            if not last_scraped_result:
                return render(
                    request,
                    "backoffice/scrape_first.html",
                    {"message": "Please scrape the latest results first."},
                )

            if isinstance(last_scraped_result.draw_date, str):
                last_scraped_date = datetime.datetime.strptime(
                    last_scraped_result.draw_date, "%Y/%m/%d"
                )
            else:
                last_scraped_date = last_scraped_result.draw_date
            # Strictly predict on same day as scraped
            if last_scraped_date.strftime("%Y/%m/%d") != today_str:
                return render(
                    request,
                    "backoffice/scrape_first.html",
                    {"message": "Please scrape the latest results first."},
                )

            data = EuroMillionsResult.objects.values(
                "ball_1",
                "ball_2",
                "ball_3",
                "ball_4",
                "ball_5",
                "lucky_star_1",
                "lucky_star_2",
            )
            df = pd.DataFrame(list(data))

            X = df.drop(["lucky_star_1", "lucky_star_2"], axis=1)
            y_balls = df[["ball_1", "ball_2", "ball_3", "ball_4", "ball_5"]]
            y_lucky = df[["lucky_star_1", "lucky_star_2"]]

            X_arr = X.values
            y_balls_arr = y_balls.values
            y_lucky_arr = y_lucky.values

            X_train_balls, X_test_balls, y_train_balls, y_test_balls = (
                train_test_split(
                    X_arr, y_balls_arr, test_size=0.3, random_state=42
                )
            )
            X_train_lucky, X_test_lucky, y_train_lucky, y_test_lucky = (
                train_test_split(
                    X_arr, y_lucky_arr, test_size=0.3, random_state=42
                )
            )

            rf_classifier_balls = RandomForestClassifier(
                n_estimators=100, random_state=42
            )
            rf_classifier_lucky = RandomForestClassifier(
                n_estimators=100, random_state=42
            )
            rf_classifier_balls.fit(X_train_balls, y_train_balls)
            rf_classifier_lucky.fit(X_train_lucky, y_train_lucky)

            unique_balls_sets = set()
            unique_full_sets = set()
            predictions = []

            for _ in range(100):
                if len(predictions) >= len(X_test_balls):
                    break
                y_pred_balls = rf_classifier_balls.predict(X_test_balls)
                y_pred_lucky = rf_classifier_lucky.predict(X_test_lucky)

                for ball_pred, lucky_pred in zip(y_pred_balls, y_pred_lucky):
                    if len(set(ball_pred)) == 5 and len(set(lucky_pred)) == 2:
                        ball_set = tuple(sorted(ball_pred))
                        lucky_set = tuple(sorted(lucky_pred))
                        full_set = ball_set + lucky_set

                        if (
                            ball_set not in unique_balls_sets
                            and full_set not in unique_full_sets
                        ):
                            unique_balls_sets.add(ball_set)
                            unique_full_sets.add(full_set)
                            prediction = Prediction(
                                prediction_date=today_str,
                                draw_date=draw_date_str,
                                pred_ball_1=ball_pred[0],
                                pred_ball_2=ball_pred[1],
                                pred_ball_3=ball_pred[2],
                                pred_ball_4=ball_pred[3],
                                pred_ball_5=ball_pred[4],
                                pred_lucky_1=lucky_pred[0],
                                pred_lucky_2=lucky_pred[1],
                            )
                            prediction.save()
                            predictions.append(prediction)

            return render(
                request,
                "backoffice/new_predictions.html",
                {"message": "New predictions added to the database."},
            )

        except Exception as e:
            return HttpResponseServerError(f"An error occurred: {e}")

    else:
        return render(request, "backoffice/backoffice.html")


@admin_required
@csrf_protect
def upload_image(request):
    if request.method == "POST":
        if "confirm" in request.POST:
            confirmation_form = OverwriteConfirmationForm(request.POST)
            if confirmation_form.is_valid():
                file_name = confirmation_form.cleaned_data["file_name"]
                temp_file_path = request.session.get("temp_file_path")
                if temp_file_path:
                    upload_result = cloudinary.uploader.upload(
                        temp_file_path, public_id=file_name, overwrite=True
                    )
                    if upload_result:
                        existing_file = UploadImageModel.objects.get(
                            name=file_name
                        )
                        existing_file.image = upload_result["secure_url"]
                        existing_file.save()
                        os.remove(temp_file_path)
                        messages.success(
                            request, f"File {file_name} was overwritten."
                        )
                        request.session.pop("temp_file_path")
                        return redirect("upload_success")
        else:
            form = UploadImageForm(request.POST, request.FILES)
            if form.is_valid():
                file_name = form.cleaned_data["name"]
                file = form.cleaned_data["image"]
                if UploadImageModel.objects.filter(name=file_name).exists():
                    temp_file = tempfile.NamedTemporaryFile(delete=False)
                    for chunk in file.chunks():
                        temp_file.write(chunk)
                    temp_file.close()
                    request.session["temp_file_path"] = temp_file.name
                    confirmation_form = OverwriteConfirmationForm(
                        initial={"file_name": file_name}
                    )
                    return render(
                        request,
                        "upload/confirm_overwrite.html",
                        {
                            "confirmation_form": confirmation_form,
                            "file_name": file_name,
                        },
                    )
                else:
                    upload_result = cloudinary.uploader.upload(
                        file, public_id=file_name, overwrite=True
                    )
                    if upload_result:
                        UploadImageModel.objects.create(
                            name=file_name, image=upload_result["secure_url"]
                        )
                        messages.success(
                            request,
                            f"File {file_name} was uploaded successfully.",
                        )
                    return redirect("upload_success")
    else:
        form = UploadImageForm()
    return render(request, "upload/upload_image.html", {"form": form})


def upload_success(request):
    return render(request, "upload/upload_success.html")


def get_image_url(name):
    image = UploadImageModel.objects.filter(name=name).values("image").first()
    return image["image"] if image else None


@admin_required
@csrf_protect
def generate_shuffled_predictions(request):
    """
    A view to generate shuffled predictions based on the latest predictions.

    This view handles POST requests to generate a set number of shuffled predictions from the latest set of predictions.
    It fetches the latest predictions, extracts the unique balls and lucky stars, and generates new shuffled predictions
    by randomly selecting and shuffling these numbers. Each unique combination of balls and lucky stars is saved as a
    new ShuffledPrediction. A success message is added upon completion.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the 'backoffice/backoffice.html' template with a success message if predictions
        were successfully generated, or an error message if no predictions were found.
    """
    if request.method == "POST":
        latest_prediction_date = Prediction.objects.aggregate(
            Max("prediction_date")
        )["prediction_date__max"]
        if not latest_prediction_date:
            return HttpResponseBadRequest("No predictions found.")

        latest_predictions = Prediction.objects.filter(
            prediction_date=latest_prediction_date
        )
        if not latest_predictions.exists():
            return HttpResponseBadRequest(
                "No predictions found for the latest date."
            )

        unique_combinations = set()
        shuffled_predictions = []

        all_balls = set()
        all_lucky_stars = set()

        for prediction in latest_predictions:
            all_balls.update(
                [
                    prediction.pred_ball_1,
                    prediction.pred_ball_2,
                    prediction.pred_ball_3,
                    prediction.pred_ball_4,
                    prediction.pred_ball_5,
                ]
            )
            all_lucky_stars.update(
                [prediction.pred_lucky_1, prediction.pred_lucky_2]
            )

        all_balls = list(all_balls)
        all_lucky_stars = list(all_lucky_stars)

        while len(shuffled_predictions) < 50:
            new_balls = sorted(random.sample(all_balls, 5))
            new_lucky_stars = sorted(random.sample(all_lucky_stars, 2))

            balls_tuple = tuple(new_balls)
            lucky_stars_tuple = tuple(new_lucky_stars)
            full_set = balls_tuple + lucky_stars_tuple

            if full_set not in unique_combinations:
                unique_combinations.add(full_set)
                shuffled_prediction = ShuffledPrediction(
                    prediction_date=latest_prediction_date,
                    draw_date=latest_predictions.first().draw_date,
                    pred_ball_1=new_balls[0],
                    pred_ball_2=new_balls[1],
                    pred_ball_3=new_balls[2],
                    pred_ball_4=new_balls[3],
                    pred_ball_5=new_balls[4],
                    pred_lucky_1=new_lucky_stars[0],
                    pred_lucky_2=new_lucky_stars[1],
                )
                shuffled_prediction.save()
                shuffled_predictions.append(shuffled_prediction)

        storage = messages.get_messages(request)
        storage.used = True
        messages.success(
            request, "Shuffled predictions generated successfully!"
        )

        return render(request, "backoffice/backoffice.html")
    else:
        return render(request, "backoffice/backoffice.html")


def display_combination_predictions(request):
    """
    A view to display the most recent shuffled predictions.

    This view fetches the latest prediction date from the ShuffledPrediction model,
    retrieves all shuffled predictions for that date, and prepares the necessary
    image URLs for each prediction. The context containing the predictions and their
    associated images is then passed to the 'shuffled_predictions/shuffled_predictions.html'
    template for rendering.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered 'shuffled_predictions/shuffled_predictions.html' template with
        the context containing predictions_with_images.
    """
    if not Subscription.objects.filter(
        Q(
            user=request.user,
            active=True,
            product_name="AI Predictions for EuroMillions Lotto",
        )
        | Q(user=request.user, active=True, product_name="Premium Full Access")
    ).exists():
        messages.error(
            request,
            "Access denied. You are not subscribed to AI Predictions or Premium Full Access.",
        )
        return redirect("pricing_page")

    latest_date = ShuffledPrediction.objects.aggregate(
        latest_date=Max("prediction_date")
    )["latest_date"]
    predictions = ShuffledPrediction.objects.filter(
        prediction_date=latest_date
    )

    image_cache = {}

    def get_cached_image_url(value):
        if value not in image_cache:
            image_cache[value] = get_image_url(value)
        return image_cache[value]

    predictions_with_images = []
    for prediction in predictions:
        pred_ball_images = [
            get_cached_image_url(f"{getattr(prediction, f'pred_ball_{i}'):02}")
            for i in range(1, 6)
        ]
        pred_lucky_images = [
            get_cached_image_url(
                f"star{getattr(prediction, f'pred_lucky_{i}')}"
            )
            for i in range(1, 3)
        ]

        predictions_with_images.append(
            {
                "prediction": prediction,
                "pred_ball_1_image": pred_ball_images[0],
                "pred_ball_2_image": pred_ball_images[1],
                "pred_ball_3_image": pred_ball_images[2],
                "pred_ball_4_image": pred_ball_images[3],
                "pred_ball_5_image": pred_ball_images[4],
                "pred_lucky_1_image": pred_lucky_images[0],
                "pred_lucky_2_image": pred_lucky_images[1],
            }
        )

    return render(
        request,
        "combination_predictions/combination_predictions.html",
        {"predictions_with_images": predictions_with_images},
    )
