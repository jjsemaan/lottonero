from django.shortcuts import render
from scraping.models import EuroMillionsResult
from predictions.models import Prediction, ShuffledPrediction, UploadImageModel
from django.db.models import Max

def get_image_url(name):
    image = UploadImageModel.objects.filter(name=name).values('image').first()
    return image['image'] if image else None

def index(request):
    """
    A view to return the index page with the latest draw results and latest winning predictions.

    This view fetches the latest EuroMillions draw result from the database. It also identifies the 
    latest prediction date where predictions have a non-null match type and fetches all predictions 
    for that date. Additionally, it fetches all winning predictions. The context containing the latest 
    draw result, latest predictions, and winning predictions is then passed to the 'index.html' template 
    for rendering.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered 'index.html' template with the context containing latest_result, 
        latest_predictions, and winning_predictions.
    """    
    
    try:
        latest_result = EuroMillionsResult.objects.latest('id')
    except EuroMillionsResult.DoesNotExist:
        latest_result = None

    # Get the latest prediction date with non-null match_type
    latest_date = Prediction.objects.filter(match_type__isnull=False).aggregate(latest_date=Max('prediction_date'))['latest_date']
    
    # Fetch all predictions with the latest date and non-null match_type
    if latest_date:
        latest_predictions = Prediction.objects.filter(prediction_date=latest_date, match_type__isnull=False)
    else:
        latest_predictions = []
    
    # Fetch all winning predictions where match_type is not null, sorted by draw_date in descending order
    alltime_winning_predictions = Prediction.objects.filter(match_type__isnull=False).order_by('-draw_date')

    # Fetch images for the latest result balls and stars
    if latest_result:
        ball_1_image = get_image_url(f"{latest_result.ball_1:02}")
        ball_2_image = get_image_url(f"{latest_result.ball_2:02}")
        ball_3_image = get_image_url(f"{latest_result.ball_3:02}")
        ball_4_image = get_image_url(f"{latest_result.ball_4:02}")
        ball_5_image = get_image_url(f"{latest_result.ball_5:02}")

        star_1_image = get_image_url(f"star{latest_result.lucky_star_1}")
        star_2_image = get_image_url(f"star{latest_result.lucky_star_2}")
    else:
        ball_1_image = ball_2_image = ball_3_image = ball_4_image = ball_5_image = None
        star_1_image = star_2_image = None

    predictions_with_images = []
    for prediction in latest_predictions:
        winning_balls_list = [int(ball) for ball in prediction.winning_balls.split(',')] if prediction.winning_balls else []
        winning_stars_list = [int(star) for star in prediction.winning_lucky_stars.split(',')] if prediction.winning_lucky_stars else []

        pred_ball_1_image = get_image_url(f"green{prediction.pred_ball_1:02}" if prediction.pred_ball_1 in winning_balls_list else f"{prediction.pred_ball_1:02}")
        pred_ball_2_image = get_image_url(f"green{prediction.pred_ball_2:02}" if prediction.pred_ball_2 in winning_balls_list else f"{prediction.pred_ball_2:02}")
        pred_ball_3_image = get_image_url(f"green{prediction.pred_ball_3:02}" if prediction.pred_ball_3 in winning_balls_list else f"{prediction.pred_ball_3:02}")
        pred_ball_4_image = get_image_url(f"green{prediction.pred_ball_4:02}" if prediction.pred_ball_4 in winning_balls_list else f"{prediction.pred_ball_4:02}")
        pred_ball_5_image = get_image_url(f"green{prediction.pred_ball_5:02}" if prediction.pred_ball_5 in winning_balls_list else f"{prediction.pred_ball_5:02}")

        pred_lucky_1_image = get_image_url(f"greenstar{prediction.pred_lucky_1}" if prediction.pred_lucky_1 in winning_stars_list else f"star{prediction.pred_lucky_1}")
        pred_lucky_2_image = get_image_url(f"greenstar{prediction.pred_lucky_2}" if prediction.pred_lucky_2 in winning_stars_list else f"star{prediction.pred_lucky_2}")

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

    # Get the latest shuffled prediction date with non-null match_type
    latest_shuffled_date = ShuffledPrediction.objects.filter(match_type__isnull=False).aggregate(latest_date=Max('prediction_date'))['latest_date']
    
    # Fetch all shuffled predictions with the latest date and non-null match_type
    if latest_shuffled_date:
        latest_shuffled_predictions = ShuffledPrediction.objects.filter(prediction_date=latest_shuffled_date, match_type__isnull=False)
    else:
        latest_shuffled_predictions = []
    
    # Fetch all winning shuffled predictions where match_type is not null, sorted by draw_date in descending order
    alltime_winning_shuffled_predictions = ShuffledPrediction.objects.filter(match_type__isnull=False).order_by('-draw_date')

    shuffled_predictions_with_images = []
    for prediction in latest_shuffled_predictions:
        winning_balls_list = [int(ball) for ball in prediction.winning_balls.split(',')] if prediction.winning_balls else []
        winning_stars_list = [int(star) for star in prediction.winning_lucky_stars.split(',')] if prediction.winning_lucky_stars else []

        pred_ball_1_image = get_image_url(f"green{prediction.pred_ball_1:02}" if prediction.pred_ball_1 in winning_balls_list else f"{prediction.pred_ball_1:02}")
        pred_ball_2_image = get_image_url(f"green{prediction.pred_ball_2:02}" if prediction.pred_ball_2 in winning_balls_list else f"{prediction.pred_ball_2:02}")
        pred_ball_3_image = get_image_url(f"green{prediction.pred_ball_3:02}" if prediction.pred_ball_3 in winning_balls_list else f"{prediction.pred_ball_3:02}")
        pred_ball_4_image = get_image_url(f"green{prediction.pred_ball_4:02}" if prediction.pred_ball_4 in winning_balls_list else f"{prediction.pred_ball_4:02}")
        pred_ball_5_image = get_image_url(f"green{prediction.pred_ball_5:02}" if prediction.pred_ball_5 in winning_balls_list else f"{prediction.pred_ball_5:02}")

        pred_lucky_1_image = get_image_url(f"greenstar{prediction.pred_lucky_1}" if prediction.pred_lucky_1 in winning_stars_list else f"star{prediction.pred_lucky_1}")
        pred_lucky_2_image = get_image_url(f"greenstar{prediction.pred_lucky_2}" if prediction.pred_lucky_2 in winning_stars_list else f"star{prediction.pred_lucky_2}")

        shuffled_predictions_with_images.append({
            'prediction': prediction,
            'pred_ball_1_image': pred_ball_1_image,
            'pred_ball_2_image': pred_ball_2_image,
            'pred_ball_3_image': pred_ball_3_image,
            'pred_ball_4_image': pred_ball_4_image,
            'pred_ball_5_image': pred_ball_5_image,
            'pred_lucky_1_image': pred_lucky_1_image,
            'pred_lucky_2_image': pred_lucky_2_image,
        })

    context = {
        'latest_result': latest_result,
        'latest_predictions': latest_predictions,
        'alltime_winning_predictions': alltime_winning_predictions,
        'ball_1_image': ball_1_image,
        'ball_2_image': ball_2_image,
        'ball_3_image': ball_3_image,
        'ball_4_image': ball_4_image,
        'ball_5_image': ball_5_image,
        'star_1_image': star_1_image,
        'star_2_image': star_2_image,
        'predictions_with_images': predictions_with_images,
        'latest_shuffled_predictions': latest_shuffled_predictions,
        'alltime_winning_shuffled_predictions': alltime_winning_shuffled_predictions,
        'shuffled_predictions_with_images': shuffled_predictions_with_images,
    }

    return render(request, 'home/index.html', context)



from django.shortcuts import render
from predictions.models import Prediction, UploadImageModel

def alltime_winning_predictions_view(request):
    """
    A view to return the all-time winning predictions page.

    This view fetches all winning predictions from the database where match_type is not null,
    sorted by draw_date in descending order. The context containing the all-time winning predictions
    is then passed to the 'alltime.html' template for rendering.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered 'alltime.html' template with the context containing alltime_winning_predictions.
    """    
    alltime_winning_predictions = Prediction.objects.filter(match_type__isnull=False).order_by('-draw_date')

    predictions_with_images = []
    for prediction in alltime_winning_predictions:
        winning_balls_list = [int(ball) for ball in prediction.winning_balls.split(',')] if prediction.winning_balls else []
        winning_stars_list = [int(star) for star in prediction.winning_lucky_stars.split(',')] if prediction.winning_lucky_stars else []

        pred_ball_1_image = get_image_url(f"green{prediction.pred_ball_1:02}" if prediction.pred_ball_1 in winning_balls_list else f"{prediction.pred_ball_1:02}")
        pred_ball_2_image = get_image_url(f"green{prediction.pred_ball_2:02}" if prediction.pred_ball_2 in winning_balls_list else f"{prediction.pred_ball_2:02}")
        pred_ball_3_image = get_image_url(f"green{prediction.pred_ball_3:02}" if prediction.pred_ball_3 in winning_balls_list else f"{prediction.pred_ball_3:02}")
        pred_ball_4_image = get_image_url(f"green{prediction.pred_ball_4:02}" if prediction.pred_ball_4 in winning_balls_list else f"{prediction.pred_ball_4:02}")
        pred_ball_5_image = get_image_url(f"green{prediction.pred_ball_5:02}" if prediction.pred_ball_5 in winning_balls_list else f"{prediction.pred_ball_5:02}")

        pred_lucky_1_image = get_image_url(f"greenstar{prediction.pred_lucky_1}" if prediction.pred_lucky_1 in winning_stars_list else f"star{prediction.pred_lucky_1}")
        pred_lucky_2_image = get_image_url(f"greenstar{prediction.pred_lucky_2}" if prediction.pred_lucky_2 in winning_stars_list else f"star{prediction.pred_lucky_2}")

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

    context = {
        'alltime_winning_predictions': predictions_with_images,
    }

    return render(request, 'home/alltime.html', context)


from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from scraping.models import EuroMillionsResult
from predictions.models import Prediction
from django.db.models import Max


def latest_predictions_with_matches(request):
    """
    A view to update the latest predictions with matching results against the latest EuroMillions draw.

    This view is triggered by a POST request. It fetches the latest draw result and the latest predictions,
    then compares each prediction's numbers against the draw numbers. It updates each prediction with the 
    match type, the matching balls, and the matching lucky stars. The updated prediction is then saved back 
    to the database.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: A simple text response indicating whether the match results were updated or if 
        the endpoint was accessed with a non-POST request.
    """
    
    if request.method == 'POST':
        latest_result = EuroMillionsResult.objects.latest('id')
        latest_date = Prediction.objects.aggregate(latest_date=Max('prediction_date'))['latest_date']
        latest_predictions = Prediction.objects.filter(prediction_date=latest_date)

        for prediction in latest_predictions:
            prediction_numbers = {
                prediction.pred_ball_1, prediction.pred_ball_2, prediction.pred_ball_3,
                prediction.pred_ball_4, prediction.pred_ball_5
            }
            draw_numbers = {
                latest_result.ball_1, latest_result.ball_2, latest_result.ball_3,
                latest_result.ball_4, latest_result.ball_5
            }
            prediction_lucky_numbers = {prediction.pred_lucky_1, prediction.pred_lucky_2}
            draw_lucky_numbers = {latest_result.lucky_star_1, latest_result.lucky_star_2}

            common_numbers = prediction_numbers & draw_numbers
            common_lucky_numbers = prediction_lucky_numbers & draw_lucky_numbers

            # Determine the match type
            match_info = determine_match_type(len(common_numbers), len(common_lucky_numbers))

            # Update the prediction instance
            if match_info:
                prediction.match_type = match_info
                prediction.winning_balls = format_numbers(common_numbers)
                prediction.winning_lucky_stars = format_numbers(common_lucky_numbers)
                prediction.save()

        return HttpResponse("Match results updated. Check the database for details.")
    else:
        return HttpResponse("This endpoint only accepts POST requests.")

def determine_match_type(num_common_numbers, num_common_lucky_numbers):
    match_cases = {
        (5, 2): 'Match 5 + 2',
        (5, 0): 'Match 5',
        (4, 2): 'Match 4 + 2',
        (4, 1): 'Match 4 + 1',
        (4, 0): 'Match 4',
        (3, 2): 'Match 3 + 2',
        (3, 1): 'Match 3 + 1',
        (3, 0): 'Match 3',
        (2, 2): 'Match 2 + 2',
        (2, 1): 'Match 2 + 1',
        (2, 0): 'Match 2',
        (1, 2): 'Match 1 + 2'
    }
    return match_cases.get((num_common_numbers, num_common_lucky_numbers))

def format_numbers(numbers):
    """Format a set of numbers as a comma-separated string, without extra commas for single numbers."""
    numbers_list = list(numbers)
    return ', '.join(map(str, numbers_list))



from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from scraping.models import EuroMillionsResult
from predictions.models import ShuffledPrediction
from django.db.models import Max

def latest_shuffled_predictions_with_matches(request):
    """
    A view to update the latest shuffled predictions with matching results against the latest EuroMillions draw.

    This view is triggered by a POST request. It fetches the latest draw result and the latest shuffled predictions,
    then compares each prediction's numbers against the draw numbers. It updates each prediction with the 
    match type, the matching balls, and the matching lucky stars. The updated prediction is then saved back 
    to the database.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: A simple text response indicating whether the match results were updated or if 
        the endpoint was accessed with a non-POST request.
    """
    
    if request.method == 'POST':
        latest_result = EuroMillionsResult.objects.latest('id')
        latest_date = ShuffledPrediction.objects.aggregate(latest_date=Max('prediction_date'))['latest_date']
        latest_predictions = ShuffledPrediction.objects.filter(prediction_date=latest_date)

        for prediction in latest_predictions:
            prediction_numbers = {
                prediction.pred_ball_1, prediction.pred_ball_2, prediction.pred_ball_3,
                prediction.pred_ball_4, prediction.pred_ball_5
            }
            draw_numbers = {
                latest_result.ball_1, latest_result.ball_2, latest_result.ball_3,
                latest_result.ball_4, latest_result.ball_5
            }
            prediction_lucky_numbers = {prediction.pred_lucky_1, prediction.pred_lucky_2}
            draw_lucky_numbers = {latest_result.lucky_star_1, latest_result.lucky_star_2}

            common_numbers = prediction_numbers & draw_numbers
            common_lucky_numbers = prediction_lucky_numbers & draw_lucky_numbers

            # Determine the match type
            match_info = determine_match_type(len(common_numbers), len(common_lucky_numbers))

            # Update the prediction instance
            if match_info:
                prediction.match_type = match_info
                prediction.winning_balls = format_numbers(common_numbers)
                prediction.winning_lucky_stars = format_numbers(common_lucky_numbers)
                prediction.save()

        return HttpResponse("Match results updated. Check the database for details.")
    else:
        return HttpResponse("This endpoint only accepts POST requests.")

def determine_match_type(num_common_numbers, num_common_lucky_numbers):
    match_cases = {
        (5, 2): 'Match 5 + 2',
        (5, 0): 'Match 5',
        (4, 2): 'Match 4 + 2',
        (4, 1): 'Match 4 + 1',
        (4, 0): 'Match 4',
        (3, 2): 'Match 3 + 2',
        (3, 1): 'Match 3 + 1',
        (3, 0): 'Match 3',
        (2, 2): 'Match 2 + 2',
        (2, 1): 'Match 2 + 1',
        (2, 0): 'Match 2',
        (1, 2): 'Match 1 + 2'
    }
    return match_cases.get((num_common_numbers, num_common_lucky_numbers))




