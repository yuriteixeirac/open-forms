from django.core.exceptions import ValidationError
from django import forms

# TODO: Implement password validation middleware

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True, min_length=8)


    def clean(self) -> dict:
        cleaned_data = super().clean()

        email, password = cleaned_data.values()

        if not (email and password):
            raise ValidationError('E-mail or password are invalid')

        return cleaned_data
