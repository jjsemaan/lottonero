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

        matches = []
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
            num_common_numbers = len(common_numbers)
            num_common_lucky_numbers = len(common_lucky_numbers)

            match_info = {
                'prediction_id': prediction.id,
                'match_info': None
            }

            if num_common_numbers == 5 and num_common_lucky_numbers == 2:
                match_info['match_info'] = 'Match 5 + 2'
            elif num_common_numbers == 5:
                match_info['match_info'] = 'Match 5'
            elif num_common_numbers == 4 and num_common_lucky_numbers == 2:
                match_info['match_info'] = 'Match 4 + 2'
            elif num_common_numbers == 4 and num_common_lucky_numbers == 1:
                match_info['match_info'] = 'Match 4 + 1'
            elif num_common_numbers == 4:
                match_info['match_info'] = 'Match 4'
            elif num_common_numbers == 3 and num_common_lucky_numbers == 2:
                match_info['match_info'] = 'Match 3 + 2'
            elif num_common_numbers == 3 and num_common_lucky_numbers == 1:
                match_info['match_info'] = 'Match 3 + 1'
            elif num_common_numbers == 3:
                match_info['match_info'] = 'Match 3'
            elif num_common_numbers == 2 and num_common_lucky_numbers == 2:
                match_info['match_info'] = 'Match 2 + 2'
            elif num_common_numbers == 2 and num_common_lucky_numbers == 1:
                match_info['match_info'] = 'Match 2 + 1'
            elif num_common_numbers == 2:
                match_info['match_info'] = 'Match 2'
            elif num_common_numbers == 1 and num_common_lucky_numbers == 2:
                match_info['match_info'] = 'Match 1 + 2'

            if match_info['match_info']:
                matches.append(match_info)
                print(f"Match found: {match_info}")  # Output to the terminal

        return HttpResponse("Check terminal for match results.")
    else:
        return HttpResponse("This endpoint only accepts POST requests.")

