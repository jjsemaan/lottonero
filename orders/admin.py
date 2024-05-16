from django.contrib import admin
from .models import Subscription, SubscriptionType

class SubscriptionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'subscription_type', 'price')
    search_fields = ('name', 'subscription_type')

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_type', 'subscribe_end_date', 'created_on')
    search_fields = ('user__username', 'subscription_type__name')

admin.site.register(SubscriptionType, SubscriptionTypeAdmin)
admin.site.register(Subscription, SubscriptionAdmin)