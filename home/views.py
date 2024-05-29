from django.shortcuts import render
from scraping.models import EuroMillionsResult
from predictions.models import Prediction
from django.db.models import Max


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

    context = {
        'latest_result': latest_result,
        'latest_predictions': latest_predictions,
        'alltime_winning_predictions': alltime_winning_predictions,
    }

    return render(request, 'home/index.html', context)

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

    context = {
        'alltime_winning_predictions': alltime_winning_predictions,
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