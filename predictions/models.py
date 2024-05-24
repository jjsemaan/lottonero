from django.db import models

class Prediction(models.Model):
    prediction_date = models.CharField(max_length=10)  # YYYY/MM/DD format
    draw_date = models.DateField(null=True, blank=True)  # New field for draw date
    pred_ball_1 = models.IntegerField()
    pred_ball_2 = models.IntegerField()
    pred_ball_3 = models.IntegerField()
    pred_ball_4 = models.IntegerField()
    pred_ball_5 = models.IntegerField()
    pred_lucky_1 = models.IntegerField()
    pred_lucky_2 = models.IntegerField()
    
    # New fields for match results
    match_type = models.CharField(max_length=100, blank=True, null=True)
    winning_balls = models.CharField(max_length=50, blank=True, null=True)  # Stored as a string
    winning_lucky_stars = models.CharField(max_length=50, blank=True, null=True)  # Stored as a string

    def __str__(self):
        return f"Prediction on {self.prediction_date} - {self.match_type if self.match_type else 'No match'}"
