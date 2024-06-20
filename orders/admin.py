from django.contrib import admin
from .models import SubscriptionType, Subscription
from tinymce.widgets import TinyMCE
from django.db import models

@admin.register(SubscriptionType)
class SubscriptionTypeAdmin(admin.ModelAdmin):
    """
    Admin interface for managing subscription types.

    Attributes:
        list_display (tuple): Fields to display in the list view.
        search_fields (tuple): Fields to include in the search functionality.
        readonly_fields (tuple): Fields that are read-only.
        ordering (tuple): Default ordering for the list view.
    """

    list_display = ('name', 'description', 'price', 'created_on', 'created_by',)
    search_fields = ('name',)
    readonly_fields = ('created_on', 'created_by',)
    ordering = ('-created_on',) 

    def save_model(self, request, obj, form, change):
        """
        Override the save method to set the created_by field during the first save.

        Args:
            request (HttpRequest): The HTTP request object.
            obj (Model): The instance being saved.
            form (ModelForm): The form used to save the instance.
            change (bool): Whether this is a change to an existing object.
        """
        if not obj.pk:  # Only set created_by during the first save
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


from django.contrib import admin
from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Admin interface for managing subscriptions.

    Attributes:
        list_display (tuple): Fields to display in the list view.
        fields (tuple): Fields to include in the form.
        search_fields (tuple): Fields to include in the search functionality.
        readonly_fields (tuple): Fields that are read-only.
        ordering (tuple): Default ordering for the list view.
    """

    list_display = ('user', 'created_on', 'email', 'active', 'interval', 'cust_id', 'invoice_id', 'subscription_id', 'prod_id')
    fields = ('user', 'created_on', 'email', 'active', 'interval', 'cust_id', 'invoice_id', 'subscription_id', 'prod_id')
    search_fields = ('user__username', 'email', 'cust_id', 'invoice_id', 'subscription_id', 'prod_id')
    readonly_fields = ('created_on',)
    ordering = ('-created_on',)

    def save_model(self, request, obj, form, change):
        """
        Override the save method to ensure the email is updated based on the user instance before saving.

        Args:
            request (HttpRequest): The HTTP request object.
            obj (Model): The instance being saved.
            form (ModelForm): The form used to save the instance.
            change (bool): Whether this is a change to an existing object.
        """
        obj.email = obj.user.email
        super().save_model(request, obj, form, change)



