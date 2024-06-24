from django.db import models
from cloudinary.models import CloudinaryField


class Prediction(models.Model):
    """
    Model representing a prediction for lottery draw results.

    Stores information about predictions made for upcoming lottery draws, including the dates, predicted numbers,
    actual outcomes if available, and any winnings associated with the predictions.

    Attributes:
        prediction_date (CharField): The date on which the prediction was made.
        draw_date (CharField): The date of the lottery draw for which the prediction applies.
        pred_ball_1 to pred_ball_5 (IntegerField): Predicted numbers for the lottery balls.
        pred_lucky_1, pred_lucky_2 (IntegerField): Predicted numbers for the lucky star balls.
        match_type (CharField): Type of match achieved by the prediction, if applicable.
        winning_balls (CharField): String representing the actual winning numbers drawn.
        winning_lucky_stars (CharField): String representing the actual winning lucky star numbers drawn.
        win_amount (DecimalField): Amount won from the prediction, if any.

    The model also includes methods for representing the prediction information as a string.
    """

    prediction_date = models.CharField(max_length=10)  # YYYY/MM/DD format
    draw_date = models.CharField(max_length=10, null=True, blank=True)
    pred_ball_1 = models.IntegerField()
    pred_ball_2 = models.IntegerField()
    pred_ball_3 = models.IntegerField()
    pred_ball_4 = models.IntegerField()
    pred_ball_5 = models.IntegerField()
    pred_lucky_1 = models.IntegerField()
    pred_lucky_2 = models.IntegerField()

    match_type = models.CharField(max_length=100, blank=True, null=True)
    winning_balls = models.CharField(max_length=50, blank=True, null=True)
    winning_lucky_stars = models.CharField(
        max_length=50, blank=True, null=True
    )

    win_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return f"Prediction on {self.prediction_date} - {self.match_type if self.match_type else 'No match'}"


class ShuffledPrediction(models.Model):
    """
    Model representing a shuffled version of lottery predictions.

    This model is similar to the Prediction model but is used specifically for storing shuffled lottery
    predictions where the predicted numbers are rearranged to analyze different outcomes.

    Attributes:
        prediction_date (CharField): The date on which the prediction was made.
        draw_date (CharField): The date of the lottery draw.
        pred_ball_1 to pred_ball_5 (IntegerField): Shuffled predicted numbers for the lottery balls.
        pred_lucky_1, pred_lucky_2 (IntegerField): Shuffled predicted numbers for the lucky star balls.
        match_type (CharField): Type of match achieved by the shuffled prediction, if applicable.
        winning_balls (CharField): Actual winning numbers drawn, stored as a string.
        winning_lucky_stars (CharField): Actual winning lucky star numbers drawn, stored as a string.
        win_amount (DecimalField): Amount won from the shuffled prediction, if any.

    The model's __str__ method provides a string representation highlighting the prediction and match type.
    """

    prediction_date = models.CharField(max_length=10)
    draw_date = models.CharField(max_length=10, null=True, blank=True)
    pred_ball_1 = models.IntegerField()
    pred_ball_2 = models.IntegerField()
    pred_ball_3 = models.IntegerField()
    pred_ball_4 = models.IntegerField()
    pred_ball_5 = models.IntegerField()
    pred_lucky_1 = models.IntegerField()
    pred_lucky_2 = models.IntegerField()

    match_type = models.CharField(max_length=100, blank=True, null=True)
    winning_balls = models.CharField(max_length=50, blank=True, null=True)
    winning_lucky_stars = models.CharField(
        max_length=50, blank=True, null=True
    )

    win_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return f"Prediction on {self.prediction_date} - {self.match_type if self.match_type else 'No match'}"


class UploadImageModel(models.Model):
    """
    Model for managing images uploaded to the cloud via Cloudinary.

    Used to store images with unique identifiers and manage them through Cloudinary's services, facilitating
    easy image uploads and management within the application.

    Attributes:
        name (CharField): Name of the image or description.
        image (CloudinaryField): Cloudinary-managed field that handles image storage, optimization, and delivery.

    The model's __str__ method returns the name of the image, simplifying identification in admin interfaces.
    """

    name = models.CharField(max_length=100)
    image = CloudinaryField("image")

    def __str__(self):
        return self.name
