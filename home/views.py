from django.shortcuts import render
from scraping.models import EuroMillionsResult

# Create your views here.

def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


def latest_draw(request):
    """ A view to return the last draw results from the db """
    latest_result = EuroMillionsResult.objects.latest('id')
    context = {
        'latest_result': latest_result,
    }
    return render(request, 'home/index.html', context)


from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from scraping.models import EuroMillionsResult
from predictions.models import Prediction
from django.db.models import Max

def latest_predictions_with_matches(request):
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
                prediction.winning_balls = str(tuple(common_numbers))
                prediction.winning_lucky_stars = str(tuple(common_lucky_numbers))
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


