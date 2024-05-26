from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class SignUpForm(UserCreationForm):
    """
    A form for creating new users.
    Extending Django's UserCreationForm to include first name,
    last name, email, phone number, and location fields.
    The form uses a Meta inner class to specify the model (User)
    and the fields to be included in the form.
    """

    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text="Optional"
        )

    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text="Optional"
        )

    email = forms.EmailField(
        max_length=254,
        help_text="Enter a valid email address"
        )

    phone_number = forms.CharField(
        max_length=15,
        required=False
        )

    location = forms.CharField(
        max_length=100,
        required=False,
        label='Address'
        )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        """
        Saves the form's data to the User model and associated Profile model.
        Args:
            commit (bool): Whether to save the user to the database.
        Returns:
            User: The newly created user instance.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            user.profile.phone_number = self.cleaned_data["phone_number"]
            user.profile.location = self.cleaned_data["location"]
            user.profile.save()
        return user


class UserForm(forms.ModelForm):
    """
    A form for updating basic user information using Django's ModelForm.
    The form allows editing the username, first name, last name, and email
    of a user.

    Attributes are defined in the Meta class, specifying which model
    and fields are used.
    """

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]


class ProfileForm(forms.ModelForm):
    """
    A form for updating user profile information, specifically phone number
    and location.

    Uses a Meta inner class to define the model (Profile)
    and fields included in the form.

    Attributes:
        phone_number (forms.CharField):
            Phone number of the user.
        location (forms.CharField):
            Location/address of the user labeled as 'Address'.
    """

    class Meta:
        model = Profile
        fields = [
            "phone_number",
            "location",
        ]

        labels = {"location": "Address"}