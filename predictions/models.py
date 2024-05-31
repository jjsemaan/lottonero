from django.db import models

class Prediction(models.Model):
    prediction_date = models.CharField(max_length=10)  # YYYY/MM/DD format
    draw_date = models.CharField(max_length=10, null=True, blank=True)  # New field for draw date
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

    # New field for win amount
    win_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Prediction on {self.prediction_date} - {self.match_type if self.match_type else 'No match'}"

class ShuffledPrediction(models.Model):
    prediction_date = models.CharField(max_length=10)  # YYYY/MM/DD format
    draw_date = models.CharField(max_length=10, null=True, blank=True)  # New field for draw date
    pred_ball_1 = models.IntegerField()
    pred_ball_2 = models.IntegerField()
    pred_ball_3 = models.IntegerField()
    pred_ball_4 = models.IntegerField()
    pred_ball_5 = models.IntegerField()
    pred_lucky_1 = models.IntegerField()
    pred_lucky_2 = models.IntegerField()
    
    def __str__(self):
        return f"Shuffled Prediction on {self.prediction_date}"

        
from cloudinary.models import CloudinaryField

class UploadImageModel(models.Model):
    name = models.CharField(max_length=100)
    image = CloudinaryField('image')

    def __str__(self):
        return self.name


