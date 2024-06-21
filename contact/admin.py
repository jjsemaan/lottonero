from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from contact.models import ContactMessage

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_email', 'message', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'email', 'message')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}" if obj.user else None

    def get_email(self, obj):
        return obj.email if obj.email else (obj.user.email if obj.user else None)

    get_full_name.short_description = 'Full Name'
    get_email.short_description = 'Email'

admin.site.register(ContactMessage, ContactMessageAdmin)