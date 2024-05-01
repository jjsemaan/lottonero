from django.contrib import admin

from django.contrib import admin
from .models import EuroMillionsResult

class EuroMillionsResultAdmin(admin.ModelAdmin):
    """
    Customizes the administration interface for EuroMillionsResult model in the Django admin site.

    Attributes:
        list_display (tuple): Specifies the fields to be displayed in the list view of EuroMillionsResult records.
        list_filter (tuple): Enables filtering of EuroMillionsResult records based on the draw_date field in the admin interface.
        search_fields (tuple): Enables searching for EuroMillionsResult records based on the draw_date field in the admin interface.

    Usage:
        This class is used to customize the display and functionality of EuroMillionsResult records
        in the Django admin interface. It specifies how the records are displayed, filtered, and searched.
    """
    
    list_display = ('draw_date', 'ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5', 'lucky_star_1', 'lucky_star_2')
    list_filter = ('draw_date',)
    search_fields = ('draw_date',)

# Register your models here.
admin.site.register(EuroMillionsResult, EuroMillionsResultAdmin)
