from django.shortcuts import render, redirect
from scraping.models import EuroMillionsResult
from .models import Prediction
from django.db.models import Max

def get_image_url(name):
    image = UploadImageModel.objects.filter(name=name).values('image').first()
    return image['image'] if image else None

def read_data_from_database(request):
    results = EuroMillionsResult.objects.all()
    # You can further process 'results' as needed
    return render(request, 'predictions/predictions.html', {'results': results})


def display_predictions(request):
    # Find the most recent prediction date
    latest_date = Prediction.objects.latest('prediction_date').prediction_date
    # Fetch all predictions with the most recent date
    predictions = Prediction.objects.filter(prediction_date=latest_date)
    
    predictions_with_images = []
    for prediction in predictions:
        pred_ball_1_image = get_image_url(f"{prediction.pred_ball_1:02}")
        pred_ball_2_image = get_image_url(f"{prediction.pred_ball_2:02}")
        pred_ball_3_image = get_image_url(f"{prediction.pred_ball_3:02}")
        pred_ball_4_image = get_image_url(f"{prediction.pred_ball_4:02}")
        pred_ball_5_image = get_image_url(f"{prediction.pred_ball_5:02}")

        pred_lucky_1_image = get_image_url(f"star{prediction.pred_lucky_1}")
        pred_lucky_2_image = get_image_url(f"star{prediction.pred_lucky_2}")

        predictions_with_images.append({
            'prediction': prediction,
            'pred_ball_1_image': pred_ball_1_image,
            'pred_ball_2_image': pred_ball_2_image,
            'pred_ball_3_image': pred_ball_3_image,
            'pred_ball_4_image': pred_ball_4_image,
            'pred_ball_5_image': pred_ball_5_image,
            'pred_lucky_1_image': pred_lucky_1_image,
            'pred_lucky_2_image': pred_lucky_2_image,
        })
    
    return render(request, 'predictions/predictions.html', {'predictions_with_images': predictions_with_images})

def backoffice(request):
    # Any logic needed to prepare context data
    return render(request, 'backoffice/backoffice.html')


from sklearn.model_selection import train_test_split 
from sklearn.ensemble import RandomForestClassifier 
import numpy as np 
import pandas as pd 
from django.views.decorators.csrf import csrf_protect 
from django.utils import timezone 
from django.http import HttpResponseBadRequest, HttpResponseServerError
import datetime
from scraping.models import EuroMillionsResult

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

    if request.method == 'POST':
        draw_date = request.POST.get('draw_date')

        if not draw_date:
            return HttpResponseBadRequest("Draw date is required.")

        # Convert the draw_date to YYYY/MM/DD format
        try:
            draw_date_obj = datetime.datetime.strptime(draw_date, '%Y-%m-%d')
            draw_date_str = draw_date_obj.strftime('%Y/%m/%d')
        except ValueError:
            return HttpResponseBadRequest("Invalid date format.")

        # Check if predictions for this draw date already exist
        if Prediction.objects.filter(draw_date=draw_date_str).exists():
            return render(request, 'backoffice/predictions_exist.html', {"message": "Predictions for this draw date already exist."})

        try:
            # Verify the last scraped draw_date
            last_scraped_result = EuroMillionsResult.objects.order_by('-draw_date').first()
            today_str = timezone.now().strftime('%Y/%m/%d')
            
            if not last_scraped_result:
                return render(request, 'backoffice/scrape_first.html', {"message": "Please scrape the latest results first."})
            
            # Convert last_scraped_result.draw_date to datetime if it's a string
            if isinstance(last_scraped_result.draw_date, str):
                last_scraped_date = datetime.datetime.strptime(last_scraped_result.draw_date, '%Y/%m/%d')
            else:
                last_scraped_date = last_scraped_result.draw_date
            
            if last_scraped_date.strftime('%Y/%m/%d') != today_str:
                return render(request, 'backoffice/scrape_first.html', {"message": "Please scrape the latest results first."})

            data = EuroMillionsResult.objects.values('ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5', 'lucky_star_1', 'lucky_star_2')
            df = pd.DataFrame(list(data))

            X = df.drop(['lucky_star_1', 'lucky_star_2'], axis=1)
            y_balls = df[['ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5']]
            y_lucky = df[['lucky_star_1', 'lucky_star_2']]

            X_arr = X.values
            y_balls_arr = y_balls.values
            y_lucky_arr = y_lucky.values

            X_train_balls, X_test_balls, y_train_balls, y_test_balls = train_test_split(X_arr, y_balls_arr, test_size=0.3, random_state=42)
            X_train_lucky, X_test_lucky, y_train_lucky, y_test_lucky = train_test_split(X_arr, y_lucky_arr, test_size=0.3, random_state=42)

            rf_classifier_balls = RandomForestClassifier(n_estimators=100, random_state=42)
            rf_classifier_lucky = RandomForestClassifier(n_estimators=100, random_state=42)
            rf_classifier_balls.fit(X_train_balls, y_train_balls)
            rf_classifier_lucky.fit(X_train_lucky, y_train_lucky)

            unique_balls_sets = set()
            unique_full_sets = set()
            predictions = []

            # Generate predictions ensuring all are unique
            for _ in range(100):  # Limit to a reasonable number of attempts
                if len(predictions) >= len(X_test_balls):
                    break
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
                                prediction_date=today_str,
                                draw_date=draw_date_str,
                                pred_ball_1=ball_pred[0],
                                pred_ball_2=ball_pred[1],
                                pred_ball_3=ball_pred[2],
                                pred_ball_4=ball_pred[3],
                                pred_ball_5=ball_pred[4],
                                pred_lucky_1=lucky_pred[0],
                                pred_lucky_2=lucky_pred[1]
                            )
                            prediction.save()
                            predictions.append(prediction)

            return render(request, 'backoffice/new_predictions.html', {"message": "New predictions added to the database."})

        except Exception as e:
            return HttpResponseServerError(f"An error occurred: {e}")

    else:
        return render(request, 'backoffice/backoffice.html')


from django.shortcuts import render, redirect
from .forms import UploadImageForm, OverwriteConfirmationForm
from .models import UploadImageModel
from django.contrib import messages
import cloudinary.uploader
import os
import tempfile

def upload_image(request):
    if request.method == 'POST':
        if 'confirm' in request.POST:
            # Handle the confirmation form submission
            confirmation_form = OverwriteConfirmationForm(request.POST)
            if confirmation_form.is_valid():
                file_name = confirmation_form.cleaned_data['file_name']
                temp_file_path = request.session.get('temp_file_path')
                if temp_file_path:
                    upload_result = cloudinary.uploader.upload(temp_file_path, public_id=file_name, overwrite=True)
                    if upload_result:
                        existing_file = UploadImageModel.objects.get(name=file_name)
                        existing_file.image = upload_result['secure_url']  # Use secure_url to save the actual URL
                        existing_file.save()
                        os.remove(temp_file_path)  # Clean up the temp file
                        messages.success(request, f"File {file_name} was overwritten.")
                        request.session.pop('temp_file_path')  # Clear the temp file path from the session
                        return redirect('upload_success')
        else:
            form = UploadImageForm(request.POST, request.FILES)
            if form.is_valid():
                file_name = form.cleaned_data['name']
                file = form.cleaned_data['image']
                if UploadImageModel.objects.filter(name=file_name).exists():
                    # Save the file to a temporary location
                    temp_file = tempfile.NamedTemporaryFile(delete=False)
                    for chunk in file.chunks():
                        temp_file.write(chunk)
                    temp_file.close()
                    request.session['temp_file_path'] = temp_file.name
                    # Render a confirmation form
                    confirmation_form = OverwriteConfirmationForm(initial={'file_name': file_name})
                    return render(request, 'upload/confirm_overwrite.html', {
                        'confirmation_form': confirmation_form,
                        'file_name': file_name
                    })
                else:
                    upload_result = cloudinary.uploader.upload(file, public_id=file_name, overwrite=True)
                    if upload_result:
                        UploadImageModel.objects.create(name=file_name, image=upload_result['secure_url'])  # Use secure_url to save the actual URL
                        messages.success(request, f"File {file_name} was uploaded successfully.")
                    return redirect('upload_success')
    else:
        form = UploadImageForm()
    return render(request, 'upload/upload_image.html', {'form': form})

def upload_success(request):
    return render(request, 'upload/upload_success.html')


from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .models import Prediction, ShuffledPrediction, UploadImageModel
from django.db.models import Max
import random

def get_image_url(name):
    image = UploadImageModel.objects.filter(name=name).values('image').first()
    return image['image'] if image else None

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

        while len(shuffled_predictions) < 30:
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
        messages.success(request, 'Shuffled predictions generated successfully!')

        return render(request, 'backoffice/backoffice.html')
    else:
        return render(request, 'backoffice/backoffice.html')

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
    # Find the most recent prediction date
    latest_date = ShuffledPrediction.objects.latest('prediction_date').prediction_date
    # Fetch all shuffled predictions with the most recent date
    predictions = ShuffledPrediction.objects.filter(prediction_date=latest_date)
    
    predictions_with_images = []
    for prediction in predictions:
        pred_ball_1_image = get_image_url(f"{prediction.pred_ball_1:02}")
        pred_ball_2_image = get_image_url(f"{prediction.pred_ball_2:02}")
        pred_ball_3_image = get_image_url(f"{prediction.pred_ball_3:02}")
        pred_ball_4_image = get_image_url(f"{prediction.pred_ball_4:02}")
        pred_ball_5_image = get_image_url(f"{prediction.pred_ball_5:02}")

        pred_lucky_1_image = get_image_url(f"star{prediction.pred_lucky_1}")
        pred_lucky_2_image = get_image_url(f"star{prediction.pred_lucky_2}")

        predictions_with_images.append({
            'prediction': prediction,
            'pred_ball_1_image': pred_ball_1_image,
            'pred_ball_2_image': pred_ball_2_image,
            'pred_ball_3_image': pred_ball_3_image,
            'pred_ball_4_image': pred_ball_4_image,
            'pred_ball_5_image': pred_ball_5_image,
            'pred_lucky_1_image': pred_lucky_1_image,
            'pred_lucky_2_image': pred_lucky_2_image,
        })
    
    return render(request, 'combination_predictions/combination_predictions.html', {'predictions_with_images': predictions_with_images})


