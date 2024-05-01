from django.db import models

class EuroMillionsResult(models.Model):
    draw_date = models.CharField(max_length=10)
    ball_1 = models.IntegerField()   
    ball_2 = models.IntegerField()
    ball_3 = models.IntegerField()
    ball_4 = models.IntegerField()
    ball_5 = models.IntegerField()
    lucky_star_1 = models.IntegerField()
    lucky_star_2 = models.IntegerField()

    def __str__(self):
        return f"{self.draw_date}: {self.ball_1}, {self.ball_2}, {self.ball_3}, {self.ball_4}, {self.ball_5}, {self.lucky_star_1}, {self.lucky_star_2}"
