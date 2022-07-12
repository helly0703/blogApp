from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Account



class DateInput(forms.DateInput):
    input_type = 'date'


# User Registration form

class UserRegisterForm(UserCreationForm):
    """
    Form for user registration
    Used form provided by django
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



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
        # Using widget for dateinput field
        widgets = {
            'birthday': DateInput(),
        }


class AccountSettingsForm(forms.ModelForm):
    """
    Form to update settings
    """

    class Meta:
        model = Account
        fields = ['privacy_mode', 'allow_notification']
