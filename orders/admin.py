from django.contrib import admin
from .models import SubscriptionType, Subscription
from tinymce.widgets import TinyMCE
from django.db import models

class SubscriptionTypeAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    list_display = ('name', 'subscription_type', 'price')
    search_fields = ('name', 'subscription_type')

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_type', 'subscribe_end_date', 'created_on')
    search_fields = ('user__username', 'subscription_type__name')

admin.site.register(SubscriptionType, SubscriptionTypeAdmin)
admin.site.register(Subscription, SubscriptionAdmin)