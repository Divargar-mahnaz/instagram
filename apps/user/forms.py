from django import forms
from django.core.exceptions import ValidationError

from apps.user.models import User
from common.constant import PHONE_PATTERN, EMAIL_PATTERN


class SignUpForm(forms.ModelForm):
    """
    this Form create for sign up with two field username and password
    """
    # for give contact info from user
    contact = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['full_name', 'user_name', 'password']

    def clean_contact(self):
        """
        set validation for contact field that most be in email or phone format
        """
        import re
        contact = self.cleaned_data['contact']
        if not (re.search(EMAIL_PATTERN, contact) or re.search(PHONE_PATTERN, contact)):
            raise ValidationError('In ValidContact Info')
        return self.cleaned_data['contact']


class LoginForm(forms.ModelForm):
    """
    this form don`t do any special work and can be switch to simple for in front only for give user and pass
    """

    class Meta:
        model = User
        fields = ['user_name', 'password']
