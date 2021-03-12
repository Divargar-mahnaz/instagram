from apps.user.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class SignUpForm(UserCreationForm):
    """
    this Form create for sign up with two field username and password
    """

    class Meta:
        model = User
        fields = ['full_name', 'user_name', 'email', 'phone_number']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('email') is None and cleaned_data.get('phone_number') is None:
            self._errors['email'] = self._errors.get('email', [])
            self._errors['email'].append('Please Enter Email or Phone number')
        return cleaned_data


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('user_name', 'full_name', 'gender', 'bio', 'image', 'website', 'phone_number', 'email')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['image'] is None or cleaned_data['image'] == False:
            cleaned_data['image'] = 'user/default_profile.png'
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        del self.fields['password']
