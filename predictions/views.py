from datetime import datetime
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
    Retrieves the URL of an image by its name from the UploadImageModel,
    accessible only to admin users.
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
    Displays lottery predictions with associated images only to subscribed
    users.

    This view checks if the user has active subscriptions to certain products
    necessary for accessing AI predictions. If not subscribed, the user is
    redirected to the pricing page. Otherwise, it retrieves the latest
    predictions, caches and retrieves associated images, and presents these
    formatted predictions on a web page.

    Args:
        request (HttpRequest): The HttpRequest object containing metadata
        about the request.

    Returns:
        HttpResponse: Renders a template with predictions and their
        corresponding images if authorized, or redirects to the pricing page
        if access is denied.
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


from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.http import HttpResponseServerError, HttpResponse
from django.shortcuts import render
from django.contrib import messages
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from scraping.models import EuroMillionsResult
from predictions.models import Prediction, ShuffledPrediction
from django.contrib.admin.views.decorators import staff_member_required

@admin_required
@csrf_protect
def train_classifier(request):
    if request.method != "POST":
        return render(request, "backoffice/backoffice.html")

    draw_date = request.POST.get("draw_date")
    if not draw_date:
        messages.error(request, "Draw date is required.")
        return render(request, "backoffice/backoffice.html")

    # Ensure the format is YYYY/MM/DD by replacing hyphens with slashes
    draw_date_str = draw_date.replace('-', '/')

    # Check if predictions for this draw date already exist
    if Prediction.objects.filter(draw_date=draw_date_str).exists():
        messages.error(request, "Predictions for this draw date already exist.")
        return render(request, "backoffice/backoffice.html")

    # Get the last draw date from the EuroMillionsResult table
    last_draw = EuroMillionsResult.objects.order_by('-draw_date').first()
    if not last_draw:
        messages.error(request, "No draw results found.")
        return render(request, "backoffice/backoffice.html")
    
    # Get the last draw date from the Prediction table
    last_prediction = Prediction.objects.order_by('-draw_date').first()

    # Ensure the format is YYYY/MM/DD by replacing hyphens with slashes
    draw_date_str = draw_date.replace('-', '/')
    last_draw_date_str = last_draw.draw_date
    last_prediction_date_str = last_prediction.draw_date if last_prediction else None

    # Check if the last draw date in EuroMillionsResult does not exist in the Prediction table
    if last_prediction_date_str != last_draw_date_str:
        messages.error(request, "The current upcoming draw has not been scraped yet!")
        return render(request, "backoffice/backoffice.html")

    try:
        # Load and prepare the lataset
        data = EuroMillionsResult.objects.values("ball_1", "ball_2", "ball_3", "ball_4", "ball_5", "lucky_star_1", "lucky_star_2")
        df = pd.DataFrame(list(data))
        X = df.drop(["lucky_star_1", "lucky_star_2"], axis=1)
        y_balls = df[["ball_1", "ball_2", "ball_3", "ball_4", "ball_5"]]
        y_lucky = df[["lucky_star_1", "lucky_star_2"]]

        # Train classifiers
        X_train_balls, X_test_balls, y_train_balls, y_test_balls = train_test_split(X, y_balls, test_size=0.3, random_state=42)
        X_train_lucky, X_test_lucky, y_train_lucky, y_test_lucky = train_test_split(X, y_lucky, test_size=0.3, random_state=42)
        rf_classifier_balls = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_classifier_lucky = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_classifier_balls.fit(X_train_balls, y_train_balls)
        rf_classifier_lucky.fit(X_train_lucky, y_train_lucky)

        unique_balls_sets = set()
        unique_full_sets = set()
        predictions = []

        # Generate predictions ensuring all are unique
        for _ in range(100):  # Limit to a reasonable number of attempts
            y_pred_balls = rf_classifier_balls.predict(X_test_balls)
            y_pred_lucky = rf_classifier_lucky.predict(X_test_lucky)

            for ball_pred, lucky_pred in zip(y_pred_balls, y_pred_lucky):
                if len(set(ball_pred)) == 5 and len(set(lucky_pred)) == 2:
                    ball_set = tuple(sorted(ball_pred))
                    lucky_set = tuple(sorted(lucky_pred))
                    full_set = ball_set + lucky_set

                    if ball_set not in unique_balls_sets and full_set not in unique_full_sets:
                        unique_balls_sets.add(ball_set)
                        unique_full_sets.add(full_set)
                        prediction = Prediction(
                            prediction_date=timezone.now().strftime("%Y/%m/%d"),
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

        messages.success(request, "New predictions added to the database.")

        # Additional functionality for ShuffledPrediction
        if ShuffledPrediction.objects.filter(draw_date=draw_date_str).exists():
            messages.error(request, "Shuffled predictions for this draw date already exist.")
            return render(request, "backoffice/backoffice.html")

        # Query predictions where match_type is not null
        prediction_data = Prediction.objects.filter(match_type__isnull=False).values(
            "pred_ball_1", "pred_ball_2", "pred_ball_3", "pred_ball_4", "pred_ball_5",
            "pred_lucky_1", "pred_lucky_2"
        )
        prediction_df = pd.DataFrame(list(prediction_data))

        if prediction_df.empty:
            messages.error(request, "No valid past predictions found for training Shuffled Predictions.")
            return render(request, "backoffice/backoffice.html")

        # Prepare the feature and target datasets
        X = prediction_df.drop(["pred_lucky_1", "pred_lucky_2"], axis=1)
        y_balls = prediction_df[["pred_ball_1", "pred_ball_2", "pred_ball_3", "pred_ball_4", "pred_ball_5"]]
        y_lucky = prediction_df[["pred_lucky_1", "pred_lucky_2"]]

        # Train classifiers
        X_train_balls, X_test_balls, y_train_balls, y_test_balls = train_test_split(X, y_balls, test_size=0.6, random_state=42)
        X_train_lucky, X_test_lucky, y_train_lucky, y_test_lucky = train_test_split(X, y_lucky, test_size=0.6, random_state=42)
        rf_classifier_balls = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_classifier_lucky = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_classifier_balls.fit(X_train_balls, y_train_balls)
        rf_classifier_lucky.fit(X_train_lucky, y_train_lucky)

        unique_balls_sets = set()
        unique_full_sets = set()
        predictions = []

        # Generate predictions ensuring all are unique
        for _ in range(100):  # Limit to a reasonable number of attempts
            y_pred_balls = rf_classifier_balls.predict(X_test_balls)
            y_pred_lucky = rf_classifier_lucky.predict(X_test_lucky)

            for ball_pred, lucky_pred in zip(y_pred_balls, y_pred_lucky):
                if len(set(ball_pred)) == 5 and len(set(lucky_pred)) == 2:
                    ball_set = tuple(sorted(ball_pred))
                    lucky_set = tuple(sorted(lucky_pred))
                    full_set = ball_set + lucky_set

                    if ball_set not in unique_balls_sets and full_set not in unique_full_sets:
                        unique_balls_sets.add(ball_set)
                        unique_full_sets.add(full_set)
                        prediction = ShuffledPrediction(
                            prediction_date=timezone.now().strftime("%Y/%m/%d"),
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

        messages.success(request, "Combination predictions added to the database.")
        return render(request, "backoffice/backoffice.html")

    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
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
                        request.session.pop("temp_file_path")
                        messages.success(
                            request, f"File {file_name} was overwritten."
                        )
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
                    messages.error(
                        request,
                        f"File {file_name} already exists!",
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


from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Max
import random


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
    if request.method == 'POST':
        latest_prediction_date = Prediction.objects.aggregate(Max('prediction_date'))['prediction_date__max']
        if not latest_prediction_date:
            return HttpResponseBadRequest("No predictions found.")

        latest_predictions = Prediction.objects.filter(prediction_date=latest_prediction_date)
        if not latest_predictions.exists():
            return HttpResponseBadRequest("No predictions found for the latest date.")

        unique_combinations = set()
        shuffled_predictions = []

        all_balls = set()
        all_lucky_stars = set()
        
        for prediction in latest_predictions:
            all_balls.update([
                prediction.pred_ball_1, prediction.pred_ball_2, prediction.pred_ball_3,
                prediction.pred_ball_4, prediction.pred_ball_5
            ])
            all_lucky_stars.update([prediction.pred_lucky_1, prediction.pred_lucky_2])
        
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
                    pred_lucky_2=new_lucky_stars[1]
                )
                shuffled_prediction.save()
                shuffled_predictions.append(shuffled_prediction)

        # Clear other irrelevant messages and add a success message
        storage = messages.get_messages(request)
        storage.used = True
        messages.success(request, 'Combination predictions generated successfully!')

        return render(request, 'backoffice/backoffice.html')
    else:
        return render(request, 'backoffice/backoffice.html')


def display_combination_predictions(request):
    """
    A view to display the most recent shuffled predictions.

    This view fetches the latest prediction date from the ShuffledPrediction
    model, retrieves all shuffled predictions for that date, and prepares the
    necessary image URLs for each prediction. The context containing the
    predictions and their associated images is then passed to the
    'shuffled_predictions/shuffled_predictions.html' template for rendering.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered 
        'shuffled_predictions/shuffled_predictions.html'
        template with the context containing predictions_with_images.
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