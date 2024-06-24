from django.contrib import admin
from .models import Prediction, ShuffledPrediction, UploadImageModel


class PredictionAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Prediction instances in the Django admin.

    Provides a detailed display, filtering, and searching capabilities specifically tailored to handle
    the fields related to lottery predictions such as prediction dates, draw dates, predicted balls, lucky stars,
    and match types. This setup aids in the efficient management and review of lottery prediction records.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
        list_filter (tuple): Fields to filter in the admin sidebar.
        search_fields (tuple): Fields to be searchable in the admin.
        fields (tuple): Fields to display in the detail view.
        readonly_fields (tuple): Fields that are read-only in the admin.
    """

    list_display = (
        "id",
        "prediction_date",
        "draw_date",
        "pred_ball_1",
        "pred_ball_2",
        "pred_ball_3",
        "pred_ball_4",
        "pred_ball_5",
        "pred_lucky_1",
        "pred_lucky_2",
        "match_type",
        "winning_balls",
        "winning_lucky_stars",
        "win_amount",
    )
    list_filter = ("prediction_date", "draw_date", "match_type")
    search_fields = ("prediction_date", "draw_date", "match_type")
    fields = (
        "prediction_date",
        "draw_date",
        "pred_ball_1",
        "pred_ball_2",
        "pred_ball_3",
        "pred_ball_4",
        "pred_ball_5",
        "pred_lucky_1",
        "pred_lucky_2",
        "match_type",
        "winning_balls",
        "winning_lucky_stars",
        "win_amount",
    )
    readonly_fields = ("id",)


class ShuffledPredictionAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Shuffled Prediction instances.

    Facilitates the administration of shuffled prediction entries, which may include variations of
    standard predictions, with tools to filter, search, and display detailed attributes of each prediction.
    Useful for tracking and analyzing the outcomes of shuffled lottery number predictions.

    Attributes are similar to PredictionAdmin, with tailored configurations for the Shuffled Prediction model.
    """

    list_display = (
        "id",
        "prediction_date",
        "draw_date",
        "pred_ball_1",
        "pred_ball_2",
        "pred_ball_3",
        "pred_ball_4",
        "pred_ball_5",
        "pred_lucky_1",
        "pred_lucky_2",
        "match_type",
        "winning_balls",
        "winning_lucky_stars",
        "win_amount",
    )
    list_filter = ("prediction_date", "draw_date", "match_type")
    search_fields = ("prediction_date", "draw_date", "match_type")
    fields = (
        "prediction_date",
        "draw_date",
        "pred_ball_1",
        "pred_ball_2",
        "pred_ball_3",
        "pred_ball_4",
        "pred_ball_5",
        "pred_lucky_1",
        "pred_lucky_2",
        "match_type",
        "winning_balls",
        "winning_lucky_stars",
        "win_amount",
    )
    readonly_fields = ("id",)


class UploadImageModelAdmin(admin.ModelAdmin):
    """
    Admin interface for managing uploaded images through UploadImageModel.

    This class configures the admin interface to effectively manage image
    uploads, providing basic search and display functionalities.
    It's optimized for scenarios where administrators need to review
    or manage uploaded images associated with model instances.

    Attributes:
        list_display (tuple): Defines which fields are displayed in the
        list view.
        search_fields (tuple): Defines the fields that are searchable
        within the admin.
        fields (tuple): Fields to be displayed in the model's form view.
        readonly_fields (tuple): Fields that should not be modified in
        the admin interface.
    """

    list_display = ("id", "name", "image")
    search_fields = ("name",)
    fields = ("name", "image")
    readonly_fields = ("id",)


admin.site.register(Prediction, PredictionAdmin)
admin.site.register(ShuffledPrediction, ShuffledPredictionAdmin)
admin.site.register(UploadImageModel, UploadImageModelAdmin)