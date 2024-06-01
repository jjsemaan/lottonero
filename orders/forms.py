from django import forms
from .models import Subscription


class OrderForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = (
            'subscription_type',
            'subscribe_end_date',
            'subscribe_cancel_date',
            'subscribe_renewal_date',
            'subscribe_price',
            'total_price',
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        placeholders = {
            'subscription_type': 'Select subscription type',
            'subscribe_end_date': 'YYYY-MM-DD',
            'subscribe_cancel_date': 'YYYY-MM-DD',
            'subscribe_renewal_date': 'YYYY-MM-DD',
            'subscribe_price': 'Enter subscription price',
            'total_price': 'Enter total price',
        }

        if user:
            self.fields['subscription_type'].initial = None  # Example, set as needed

        self.fields['subscription_type'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field in placeholders:
                placeholder = f"{placeholders[field]}{' *' if self.fields[field].required else ''}"
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
