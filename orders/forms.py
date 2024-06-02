from django import forms
from .models import Subscription
from decimal import Decimal


class OrderForm(forms.ModelForm):
    SUBSCRIPTION_CHOICES = [
        ('monthly', 'Monthly (€ 9.99)'),
        ('annual', 'Annual (€ 102.00)'),
    ]

    subscription_option = forms.ChoiceField(
        choices=SUBSCRIPTION_CHOICES,
        widget=forms.RadioSelect,
        initial='monthly',  # Set the default value
        label="Choose your subscription"
    )

    class Meta:
        model = Subscription
        fields = (
            'subscribe_end_date',
            'subscribe_cancel_date',
            'subscribe_renewal_date',
            'total_price',
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        subscription_type = kwargs.pop('subscription_type', None)
        super().__init__(*args, **kwargs)
        placeholders = {
            'subscribe_end_date': 'Subscription End Date',
            'subscribe_cancel_date': 'YYYY-MM-DD',
            'subscribe_renewal_date': 'Subscription Renewal Date',
        }

        if subscription_type:
            self.subscription_type = subscription_type
            monthly_price = subscription_type.price
            annual_price = (monthly_price * Decimal(12) * Decimal(0.85)).quantize(Decimal('0.01'))  # 15% discount for annual subscription

            self.fields['subscription_option'].widget.choices = [
                ('monthly', f'Monthly (€ {monthly_price})'),
                ('annual', f'Annual (€ {annual_price})')
            ]

        for field in self.fields:
            if field in placeholders:
                placeholder = f"{placeholders[field]}{' *' if self.fields[field].required else ''}"
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
        
        self.fields['total_price'].widget.attrs['readonly'] = True
        self.fields['total_price'].widget.attrs['class'] += ' readonly'

    def clean_total_price(self):
        cleaned_data = super().clean()
        subscription_option = cleaned_data.get('subscription_option')

        if subscription_option:
            monthly_price = self.subscription_type.price
            annual_price = (monthly_price * Decimal(12) * Decimal(0.85)).quantize(Decimal('0.01'))  # 15% discount for annual subscription

            if subscription_option == 'monthly':
                return monthly_price
            elif subscription_option == 'annual':
                return annual_price

        return Decimal('0.00')