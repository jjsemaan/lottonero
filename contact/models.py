from django.db import models
from django.contrib.auth.models import User


class ContactMessage(models.Model):
    """
    Represents a contact message sent by users through the website.

    This model is designed to store messages from both authenticated and
    unauthenticated users. Authenticated users' messages are linked directly to their user
    account, whereas unauthenticated users must provide their full name and email address.

    Attributes:
        user (ForeignKey): A reference to the User model, nullable, for authenticated users.
        full_name (CharField): The full name of the unauthenticated user, nullable.
        email (EmailField): The email address of the unauthenticated user, nullable.
        message (TextField): The content of the message.
        created_at (DateTimeField): The date and time the message was created, automatically set when the message is saved.

    Methods:
        __str__(self): Returns a string representation of the message, including the sender's
                       email and the timestamp of when the message was sent.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    full_name = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.email if self.email else self.user.email} at {self.created_at}"
