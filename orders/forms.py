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
    first_name = forms.CharField(max_length=30, required=False, label="First Name")
    last_name = forms.CharField(max_length=30, required=False, label="Last Name")

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
        
        if subscription_type:
            self.subscription_type = subscription_type
            monthly_price = subscription_type.price
            annual_price = (monthly_price * Decimal(12) * Decimal(0.85)).quantize(Decimal('0.01'))  # 15% discount for annual subscription

            self.fields['subscription_option'].widget.choices = [
                ('monthly', f'Monthly (€ {monthly_price})'),
                ('annual', f'Annual (€ {annual_price})')
            ]

        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
        
        for field in ['first_name', 'last_name']:
            if not getattr(user, field):
                self.fields[field].required = True

        for field in self.fields:
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