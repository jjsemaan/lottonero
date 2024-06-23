from django import forms
from .models import UploadImageModel


class UploadImageForm(forms.ModelForm):
    """
    A Django form for uploading images through admin backoffice.

    This form is used to upload images that are used in various parts of the application, typically for content
    development and administrative purposes.

    Attributes:
        model (Model): The Django model that the form is associated with.
        fields (list): Fields that are included in the form.

    Note:
        This form is intended to be used in the admin interface, and access should be restricted to admin users.
    """

    class Meta:
        model = UploadImageModel
        fields = ["name", "image"]


class OverwriteConfirmationForm(forms.Form):
    confirm = forms.BooleanField(required=True, label="Confirm overwrite?")
    file_name = forms.CharField(widget=forms.HiddenInput())
