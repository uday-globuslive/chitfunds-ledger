from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, ChitFund, Payment
from django.utils import timezone


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address']


class ChitFundForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = ChitFund
        fields = ['name', 'description', 'total_amount', 'duration_months', 
                  'monthly_amount', 'organizer', 'start_date', 'end_date']
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        duration_months = cleaned_data.get('duration_months')
        
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("End date should be after start date.")
                
        if start_date and duration_months:
            # Calculate expected end date based on duration
            expected_end_date = start_date.replace(month=start_date.month + duration_months) \
                if start_date.month + duration_months <= 12 \
                else start_date.replace(year=start_date.year + ((start_date.month + duration_months - 1) // 12), 
                                        month=((start_date.month + duration_months - 1) % 12) + 1)
            
            if end_date != expected_end_date:
                cleaned_data['end_date'] = expected_end_date
                
        return cleaned_data


class PaymentForm(forms.ModelForm):
    payment_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), 
                                   initial=timezone.now)
    
    class Meta:
        model = Payment
        fields = ['amount', 'payment_date', 'payment_method', 'reference_number', 'receipt_image', 'notes']
    
    def clean_payment_date(self):
        payment_date = self.cleaned_data.get('payment_date')
        if payment_date and payment_date > timezone.now().date():
            raise forms.ValidationError("Payment date cannot be in the future.")
        return payment_date


class PaymentFilterForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    payment_method = forms.CharField(required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        
        if date_from and date_to and date_from > date_to:
            raise forms.ValidationError("End date should be after start date.")
        
        return cleaned_data
