from django.contrib import admin
from .models import Subscription
from tinymce.widgets import TinyMCE
from django.db import models


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Admin interface for managing subscriptions.

    Attributes:
        list_display (tuple): Fields to display in the list view,
        including the new 'cancelled_on' field.
        fields (tuple): Fields to include in the form, including
        the new 'cancelled_on' field.
        search_fields (tuple): Fields to include in the search functionality.
        readonly_fields (tuple): Fields that are read-only, now including
        'cancelled_on' to prevent direct editing.
        ordering (tuple): Default ordering for the list view.
    """

    list_display = (
        "user",
        "created_on",
        "email",
        "active",
        "cancelled_on",
        "interval",
        "cust_id",
        "invoice_id",
        "subscription_id",
        "prod_id",
        "product_name",
    )
    fields = (
        "user",
        "email",
        "active",
        "interval",
        "cust_id",
        "invoice_id",
        "subscription_id",
        "prod_id",
        "product_name",
    )
    search_fields = (
        "user__username",
        "email",
        "cust_id",
        "invoice_id",
        "subscription_id",
        "prod_id",
        "product_name",
    )
    readonly_fields = ("created_on", "cancelled_on")
    ordering = ("-created_on",)

    def save_model(self, request, obj, form, change):
        """
        Override the save method to ensure the email is updated based
        on the user instance before saving.

        Args:
            request (HttpRequest): The HTTP request object.
            obj (Model): The instance being saved.
            form (ModelForm): The form used to save the instance.
            change (bool): Whether this is a change to an existing object.
        """
        obj.email = obj.user.email
        super().save_model(request, obj, form, change)