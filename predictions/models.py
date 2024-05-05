from django.db import models


class Prediction(models.Model):
    prediction_date = models.CharField(max_length=10)  # YYYY/MM/DD format
    pred_ball_1 = models.IntegerField()
    pred_ball_2 = models.IntegerField()
    pred_ball_3 = models.IntegerField()
    pred_ball_4 = models.IntegerField()
    pred_ball_5 = models.IntegerField()
    pred_lucky_1 = models.IntegerField()
    pred_lucky_2 = models.IntegerField()

    def __str__(self):
        return f"Prediction on {self.prediction_date}"

