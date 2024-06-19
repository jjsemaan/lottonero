from django.contrib import admin
from .models import SubscriptionType, Subscription
from tinymce.widgets import TinyMCE
from django.db import models

@admin.register(SubscriptionType)
class SubscriptionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'created_on', 'created_by',)
    search_fields = ('name',)
    readonly_fields = ('created_on', 'created_by',)
    ordering = ('-created_on',) 

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set created_by during the first save
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

from django.contrib import admin
from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_on', 'email', 'event_id', 'prod_id')
    fields = ('user', 'created_on', 'email', 'event_id', 'prod_id')
    search_fields = ('user__username', 'email', 'event_id', 'prod_id')
    readonly_fields = ('created_on',)
    ordering = ('-created_on',)

    def save_model(self, request, obj, form, change):
        """
        Override the save method to ensure the email is updated
        based on the user instance before saving.
        """
        obj.email = obj.user.email
        super().save_model(request, obj, form, change)



