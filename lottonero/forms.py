from django import forms
from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    """
    Custom signup form extending the default django-allauth signup form to
    include first and last name fields.

    This form modifies the default signup process by adding required first
    name and last name fields.
    It ensures these additional fields are captured during the signup process
    and stored in the user model.

    Attributes:
        first_name (CharField): Input field for user's first name, required.
        last_name (CharField): Input field for user's last name, required.

    Methods:
        save(request): Overrides the save method to save the additional first
        and last names to the user model after the form is submitted and the
        user object is created.
    """

    first_name = forms.CharField(
        max_length=30,
        label="First Name",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "First Name"}),
    )
    last_name = forms.CharField(
        max_length=30,
        label="Last Name",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Last Name"}),
    )

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user