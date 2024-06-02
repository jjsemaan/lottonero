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
    list_display = ('order_number', 'subscription_type', 'user', 'created_on', 'subscribe_end_date', 'recurring_subscription')
    fields = ('order_number', 'subscription_type', 'user', 'created_on', 'subscribe_end_date', 'recurring_subscription')
    search_fields = ('user__username', 'subscription_type__name', 'order_number')
    readonly_fields = ('order_number', 'created_on')
    ordering = ('-created_on',)

    def save_model(self, request, obj, form, change):
        # Ensure the price is updated from the subscription type when saving
        if obj.subscription_type:
            obj.subscribe_price = obj.subscription_type.price
        super().save_model(request, obj, form, change)

