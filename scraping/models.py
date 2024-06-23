from django.db import models


class EuroMillionsResult(models.Model):
    """
    Represents a EuroMillions lottery draw result.

    Attributes:
        draw_date (str): The date of the lottery draw in the format 'YYYY-MM-DD'.
        ball_1 (int): The first main ball number drawn.
        ball_2 (int): The second main ball number drawn.
        ball_3 (int): The third main ball number drawn.
        ball_4 (int): The fourth main ball number drawn.
        ball_5 (int): The fifth main ball number drawn.
        lucky_star_1 (int): The first lucky star number drawn.
        lucky_star_2 (int): The second lucky star number drawn.
        jackpot (str): The jackpot amount for the draw.
        prize_breakdown (str): A detailed description of the prize distribution.

    Methods:
        __str__: Returns a string representation of the EuroMillionsResult instance.

    Usage:
        This model represents the results of EuroMillions lottery draws. Each instance
        contains the draw date along with the winning numbers, lucky stars, jackpot amount,
        and a description of the prize distribution.
    """

    draw_date = models.CharField(max_length=10)
    ball_1 = models.IntegerField()
    ball_2 = models.IntegerField()
    ball_3 = models.IntegerField()
    ball_4 = models.IntegerField()
    ball_5 = models.IntegerField()
    lucky_star_1 = models.IntegerField()
    lucky_star_2 = models.IntegerField()
    jackpot = models.CharField(max_length=100)
    prize_breakdown = models.TextField()

    def __str__(self):
        return f"{self.draw_date}: {self.ball_1}, {self.ball_2}, {self.ball_3}, {self.ball_4}, {self.ball_5}, {self.lucky_star_1}, {self.lucky_star_2}, Jackpot: {self.jackpot}"
