from django import forms
from django.contrib.auth.models import User
from .models import Member, Subscription

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['full_name', 'phone_number']

class SubscriptionRequestForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['duration']
        widgets = {
            'duration': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'duration': 'اختر مدة الاشتراك'
        }