from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Account


# User Registration form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# User Updation form
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


# For date input as calendar
class DateInput(forms.DateInput):
    input_type = 'date'


# Account Update form
class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['image', 'name', 'birthday', 'gender', 'description']
        # Using widget for dateinput field
        widgets = {
            'birthday': DateInput(),
        }

