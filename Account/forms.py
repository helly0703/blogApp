from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Account


# User Registration form

class UserRegisterForm(UserCreationForm):
    """
    Form for user registration
    Used form provided by django
    """
    email = forms.EmailField()
    birthdate = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1',
            'type': 'date',
            'min': '2000-01-01', 'max': '2022-12-31',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'birthdate', 'password1', 'password2']


# User Updation form
class UserUpdateForm(forms.ModelForm):
    """
    Form to update user model fields
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


# Account Update form
class AccountUpdateForm(forms.ModelForm):
    """
    Form to update account details
    """

    class Meta:
        model = Account
        fields = ['image', 'name', 'birthday', 'gender', 'description']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date', 'min': '2000-01-01', 'max': '2022-12-31'})
        }


class AccountSettingsForm(forms.ModelForm):
    """
    Form to update settings
    """

    class Meta:
        model = Account
        fields = ['privacy_mode', 'allow_notification']
