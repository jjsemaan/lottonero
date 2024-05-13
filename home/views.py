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

            common_numbers = prediction_numbers & draw_numbers
            if len(common_numbers) == 2:
                match_info = {
                    'prediction_id': prediction.id,
                    'match_info': 'Match 2'
                }
                matches.append(match_info)
                print(f"Match found: {match_info}")  # Output to the terminal

        return HttpResponse("Check terminal for match results.")
    else:
        return HttpResponse("This endpoint only accepts POST requests.")