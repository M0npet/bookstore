"""Форма оформлення замовлення."""
from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("full_name", "email", "phone", "address")
        labels = {
            "full_name": "Отримувач (ПІБ)",
            "email": "Email",
            "phone": "Телефон",
            "address": "Адреса доставки",
        }
        widgets = {
            "address": forms.TextInput(
                attrs={"placeholder": "Заповніть, якщо є друковані книги"}
            ),
        }
