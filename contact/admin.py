from django.contrib import admin
from .models import ContactMessage

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'message', 'created_at')
    search_fields = ('full_name', 'email', 'message')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Ensure that messages from authenticated users show the user's full name and email
        queryset = queryset.annotate(
            full_name=models.F('user__first_name') + ' ' + models.F('user__last_name'),
            email=models.F('user__email')
        )
        return queryset

    def full_name(self, obj):
        return obj.full_name if obj.full_name else f"{obj.user.first_name} {obj.user.last_name}"

    def email(self, obj):
        return obj.email if obj.email else obj.user.email

    full_name.short_description = 'Full Name'
    email.short_description = 'Email'

admin.site.register(ContactMessage, ContactMessageAdmin)

