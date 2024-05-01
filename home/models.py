from django.db import models

class LotteryResult(models.Model):
    """
    A Django database model representing the results of a 
    EuroMillions lottery draw from https://www.lottery.ie/accessible-results.

    Attributes:
        draw_date (models.CharField): The date of the lottery draw.
        winning_numbers (models.CharField): The winning numbers from the lottery draw.
        lucky_stars (models.CharField): The Lucky Stars numbers from the lottery draw.
        jackpot (models.CharField): The total jackpot amount for the draw.
        created_at (models.DateTimeField): The timestamp when the lottery result was created in the database.

    Methods:
        __str__: Returns a string representation of the model, which includes the draw date and the lottery type.
    """
    draw_date = models.CharField(max_length=100)
    winning_numbers = models.CharField(max_length=100)
    lucky_stars = models.CharField(max_length=50)
    jackpot = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.draw_date} EuroMillions"

