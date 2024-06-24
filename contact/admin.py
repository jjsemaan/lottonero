from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from contact.models import ContactMessage


class ContactMessageAdmin(admin.ModelAdmin):
    """
    Administrator interface for ContactMessage model in Django admin.

    Provides customized display options in the admin list view, including:
    - Displaying the full name of the user associated with each contact
      message, if available.
    - Displaying the user's email or the email provided in the contact message.
    - Allowing search functionality across user's first and last names, email,
      and message contents.
    - Filtering messages based on the date they were created.
    - Setting certain fields as read-only.

    Attributes:
        list_display (tuple): Defines the columns that are displayed in the
        list view.
        search_fields (tuple):
        Defines the fields on which the search can be performed.
        list_filter (tuple):
        Defines the fields that will be used for filtering the list on the
        admin page.
        readonly_fields (tuple):
        Fields that cannot be modified in the admin interface.

    Methods:
        get_full_name(self, obj): Returns the full name of the user associated
        with the message.
        get_email(self, obj): Returns the email address associated with the
        message.
    """

    list_display = ("get_full_name", "get_email", "message", "created_at")
    search_fields = ("user__first_name", "user__last_name", "email", "message")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)

    def get_full_name(self, obj):
        return (
            f"{obj.user.first_name} {obj.user.last_name}" if obj.user else None
        )

    def get_email(self, obj):
        return (
            obj.email if obj.email else (obj.user.email if obj.user else None)
        )

    get_full_name.short_description = "Full Name"
    get_email.short_description = "Email"


admin.site.register(ContactMessage, ContactMessageAdmin)
