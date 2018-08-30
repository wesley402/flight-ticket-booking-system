from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from django.contrib.auth.models import User
#from django.db.models import Profile
from django.apps import apps


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist or password wrong!!")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect passsword")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password_confirm'

        ]

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("password must match!!!")

        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            raise forms.ValidationError("This usename has already been registered")
        return super(UserRegisterForm, self).clean(*args, **kwargs)

class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'username',
            'date_joined',
            'first_name',
            'last_name',
            'email',
        )
        exclude = (
            'username',
            'date_joined',
        )
        help_texts = {
            'username': None,
            'email': None,
            'first_name': None,
            'last_name': None,
            'date_joined': None,
        }

class EditProfileForm(forms.ModelForm):
    class Meta:
        model =  apps.get_model('accounts', 'Profile')
        fields = (
            'address',
            'city',
            'state',
            'zip_code',
            'telephone',
            'credit_card',
            'seat_preference',
            'meal_preference',

        )
