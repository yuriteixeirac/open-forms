from django import forms
from django.core.validators import ValidationError
from apps.accounts.models import User


class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)


    def clean_email(self) -> str:
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if User.objects.filter(email=email).exists():   # type: ignore
            raise ValidationError('User with e-mail already exists.')

        return email


    def clean(self) -> dict:
        cleaned_data = super().clean()

        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError('Unequal password were given.')

        user_exists = User.objects.filter(email=email).exists()     # type: ignore

        if user_exists:
            raise ValidationError('User already exists.')

        return cleaned_data


    def save(self) -> User:
        user = User(email=self.cleaned_data.get('email'))
        user.set_password(self.cleaned_data.get('password'))
        user.save()

        return user
