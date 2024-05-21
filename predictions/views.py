from django.shortcuts import render
from scraping.models import EuroMillionsResult
from .models import Prediction

# Create your views here.
def read_data_from_database(request):
    results = EuroMillionsResult.objects.all()
    # You can further process 'results' as needed
    return render(request, 'predictions/predictions.html', {'results': results})


def display_predictions(request):
    # Find the most recent prediction date
    latest_date = Prediction.objects.latest('prediction_date').prediction_date
    # Fetch all predictions with the most recent date
    predictions = Prediction.objects.filter(prediction_date=latest_date)
    
    return render(request, 'predictions/predictions.html', {'predictions': predictions})

def backoffice(request):
    # Any logic needed to prepare context data
    return render(request, 'backoffice/backoffice.html')


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
from .models import Prediction
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone


@csrf_protect
def train_classifier(request):
    if request.method == 'POST':
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
        today_str = timezone.now().strftime('%Y/%m/%d')

        # Generate predictions ensuring all are unique
        for _ in range(100):  # Limit to a reasonable number of attempts
            if len(predictions) >= len(X_test_balls):
                break

            y_pred_balls = rf_classifier_balls.predict(X_test_balls)
            y_pred_lucky = rf_classifier_lucky.predict(X_test_lucky)

            for ball_pred, lucky_pred in zip(y_pred_balls, y_pred_lucky):
                if len(set(ball_pred)) == 5 and len(set(lucky_pred)) == 2:  # Check for internal uniqueness
                    ball_set = tuple(sorted(ball_pred))
                    lucky_set = tuple(sorted(lucky_pred))
                    full_set = ball_set + lucky_set

                    if ball_set not in unique_balls_sets and full_set not in unique_full_sets:
                        unique_balls_sets.add(ball_set)
                        unique_full_sets.add(full_set)
                        prediction = Prediction(
                            prediction_date=today_str,
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

        context = {'predictions': predictions}
        return render(request, 'backoffice/backoffice.html', context)
    else:
        return render(request, 'backoffice/backoffice.html')