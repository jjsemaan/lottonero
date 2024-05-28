from django import forms
from .models import UploadImageModel

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UploadImageModel
        fields = ['name', 'image']

class OverwriteConfirmationForm(forms.Form):
    confirm = forms.BooleanField(required=True, label="Confirm overwrite?")
    file_name = forms.CharField(widget=forms.HiddenInput())

