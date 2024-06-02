from django import forms
from .models import Subscription
from decimal import Decimal


class OrderForm(forms.ModelForm):
    SUBSCRIPTION_CHOICES = [
        ('monthly', 'Monthly'),
        ('annual', 'Annual'),
    ]

    subscription_option = forms.ChoiceField(
        choices=SUBSCRIPTION_CHOICES,
        widget=forms.RadioSelect,
        label="Choose your subscription"
    )

    class Meta:
        model = Subscription
        fields = ()  # Remove fields that are automatically set

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        subscription_type = kwargs.pop('subscription_type', None)
        super().__init__(*args, **kwargs)
        
        if subscription_type:
            self.subscription_type = subscription_type
            monthly_price = subscription_type.price
            annual_price = (monthly_price * Decimal(12) * Decimal(0.85)).quantize(Decimal('0.01'))

            self.fields['subscription_option'].widget.choices = [
                ('monthly', f'Monthly (€ {monthly_price})'),
                ('annual', f'Annual (€ {annual_price})')
            ]
        
        self.fields['total_price'] = forms.CharField(widget=forms.HiddenInput(), required=False)

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
