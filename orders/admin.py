from django.contrib import admin
from .models import SubscriptionType, Subscription
from tinymce.widgets import TinyMCE
from django.db import models

@admin.register(SubscriptionType)
class SubscriptionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_on', 'created_by')
    search_fields = ('name',)
    readonly_fields = ('created_on', 'created_by')  # Make created_by read-only

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set created_by during the first save
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_type', 'subscribe_end_date', 'created_on')
    search_fields = ('user__username', 'subscription_type__name')
