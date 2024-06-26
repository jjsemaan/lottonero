from django.shortcuts import render
from django.core.management import call_command
from django.contrib import messages
from scraping.models import EuroMillionsResult
from predictions.models import Prediction, ShuffledPrediction
from django.db.models import Max
from django.http import HttpResponse
import io

def run_scrape_euromillions(request):
    """
    Combines the functionality of scraping EuroMillions results, updating the latest
    predictions, and updating the latest shuffled predictions.

    This function orchestrates the following:
    1. Executes the 'scrape_euromillions' command to fetch new results.
    2. Updates regular predictions with the newly scraped data.
    3. Updates shuffled predictions accordingly.

    Args:
        request (HttpRequest): The HttpRequest object containing metadata about the request.

    Returns:
        HttpResponse: Renders the 'backoffice/backoffice.html' template displaying
        success or error messages.
    """
    # Step 1: Run the scraping process
    out = io.StringIO()
    call_command('scrape_euromillions', stdout=out)
    result = out.getvalue()

    if "have already been scraped" in result:
        messages.error(request, "No new data to scrape. All available data have already been scraped.")
    else:
        messages.success(request, "Data scraped successfully.")

        # Step 2: Update latest predictions
        update_predictions()

        # Step 3: Update latest shuffled predictions
        update_shuffled_predictions()

    return render(request, 'backoffice/backoffice.html')

def update_predictions():
    """
    Updates the latest predictions by comparing them against the latest EuroMillions draw results.
    """
    latest_result = EuroMillionsResult.objects.latest('id')
    latest_date = Prediction.objects.aggregate(latest_date=Max('prediction_date'))['latest_date']
    latest_predictions = Prediction.objects.filter(prediction_date=latest_date)
    
    for prediction in latest_predictions:
        update_prediction_with_match_results(prediction, latest_result)

def update_shuffled_predictions():
    """
    Updates the latest shuffled predictions by comparing them against the latest EuroMillions draw results.
    """
    latest_result = EuroMillionsResult.objects.latest('id')
    latest_date = ShuffledPrediction.objects.aggregate(latest_date=Max('prediction_date'))['latest_date']
    latest_predictions = ShuffledPrediction.objects.filter(prediction_date=latest_date)

    for prediction in latest_predictions:
        update_prediction_with_match_results(prediction, latest_result)

def update_prediction_with_match_results(prediction, latest_result):
    """
    Helper function to update a single prediction with the matching results from the latest draw.
    """
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

def determine_match_type(num_common_numbers, num_common_lucky_numbers):
    match_cases = {
        (5, 2): '5 + 2 Stars',
        (5, 1): '5 + 1 Stars',
        (5, 0): 'Match 5',
        (4, 2): '4 + 2 Stars',
        (4, 1): '4 + 1 Stars',
        (3, 2): '3 + 2 Stars',
        (4, 0): 'Match 4',
        (2, 2): '2 + 2 Stars',
        (3, 1): '3 + 1 Stars',
        (3, 0): 'Match 3',
        (1, 2): '1 + 2 Stars',
        (2, 1): '2 + 1 Stars',
        (2, 0): 'Match 2' 
    }
    return match_cases.get((num_common_numbers, num_common_lucky_numbers))

def format_numbers(numbers_set):
    """
    Formats the numbers set into a sorted, comma-separated string for display or storage.
    """
    return ', '.join(sorted(map(str, numbers_set)))
