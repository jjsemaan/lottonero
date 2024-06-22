from django import forms
from .models import ContactMessage


class AuthenticatedContactMessageForm(forms.ModelForm):
    """
    A form based on the ContactMessage model for authenticated users.

    This form is used to collect messages from authenticated users, assuming that the user's
    identity and contact information are already known and do not need to be provided again.
    The form only includes a field for the message content.

    Attributes:
        model (Model): The Django model associated with this form is ContactMessage.
        fields (list): Specifies the only field included in the form which is 'message'.
        widgets (dict): Defines the form widgets and their HTML attributes for the 'message' field.
    """

    class Meta:
        model = ContactMessage
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(
                attrs={"placeholder": "Your message here...", "rows": 4}
            ),
        }


class UnauthenticatedContactMessageForm(forms.ModelForm):
    """
    A form based on the ContactMessage model for unauthenticated users.

    This form is used to collect messages from unauthenticated users. It includes fields
    for the user's full name, email, and message content. If the user is unexpectedly authenticated
    (e.g., logs in during the session before submitting the form), the email field is automatically
    hidden to reflect their logged-in status, assuming their email is already known.

    Attributes:
        model (Model): The Django model associated with this form is ContactMessage.
        fields (list): Specifies the fields included in the form which are 'full_name', 'email', and 'message'.
        widgets (dict): Defines the form widgets and their HTML attributes for each field.

    Methods:
        __init__(*args, **kwargs): Extends the base initialization method to handle cases where
                                  an authenticated user might be using this form, hiding the email
                                  field if the user is authenticated.
    """

    class Meta:
        model = ContactMessage
        fields = ["full_name", "email", "message"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Full Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "message": forms.Textarea(
                attrs={"placeholder": "Your message here...", "rows": 4}
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields["email"].widget = forms.HiddenInput()
