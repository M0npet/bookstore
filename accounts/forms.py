"""Форми реєстрації та редагування профілю."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    """Форма реєстрації. Додає обов'язкове поле email до стандартної форми."""

    email = forms.EmailField(required=True, label="Електронна пошта")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Користувач з таким email уже існує.")
        return email


class ProfileForm(forms.ModelForm):
    """Форма редагування полів профілю після реєстрації."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "address", "avatar")
        labels = {
            "first_name": "Ім'я",
            "last_name": "Прізвище",
            "email": "Email",
            "phone": "Телефон",
            "address": "Адреса доставки",
            "avatar": "Аватар",
        }
