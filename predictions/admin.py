from django.contrib import admin
from .models import Prediction, ShuffledPrediction, UploadImageModel

class PredictionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'prediction_date', 'draw_date', 'pred_ball_1', 'pred_ball_2', 
        'pred_ball_3', 'pred_ball_4', 'pred_ball_5', 'pred_lucky_1', 'pred_lucky_2', 
        'match_type', 'winning_balls', 'winning_lucky_stars', 'win_amount'
    )
    list_filter = ('prediction_date', 'draw_date', 'match_type')
    search_fields = ('prediction_date', 'draw_date', 'match_type')
    fields = (
        'prediction_date', 'draw_date', 'pred_ball_1', 'pred_ball_2', 
        'pred_ball_3', 'pred_ball_4', 'pred_ball_5', 'pred_lucky_1', 'pred_lucky_2', 
        'match_type', 'winning_balls', 'winning_lucky_stars', 'win_amount'
    )
    readonly_fields = ('id',)

class ShuffledPredictionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'prediction_date', 'draw_date', 'pred_ball_1', 'pred_ball_2', 
        'pred_ball_3', 'pred_ball_4', 'pred_ball_5', 'pred_lucky_1', 'pred_lucky_2', 
        'match_type', 'winning_balls', 'winning_lucky_stars', 'win_amount'
    )
    list_filter = ('prediction_date', 'draw_date', 'match_type')
    search_fields = ('prediction_date', 'draw_date', 'match_type')
    fields = (
        'prediction_date', 'draw_date', 'pred_ball_1', 'pred_ball_2', 
        'pred_ball_3', 'pred_ball_4', 'pred_ball_5', 'pred_lucky_1', 'pred_lucky_2', 
        'match_type', 'winning_balls', 'winning_lucky_stars', 'win_amount'
    )
    readonly_fields = ('id',)

class UploadImageModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')
    search_fields = ('name',)
    fields = ('name', 'image')
    readonly_fields = ('id',)

admin.site.register(Prediction, PredictionAdmin)
admin.site.register(ShuffledPrediction, ShuffledPredictionAdmin)
admin.site.register(UploadImageModel, UploadImageModelAdmin)
