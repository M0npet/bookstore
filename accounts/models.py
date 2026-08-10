"""Модель користувача та профіль."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Власна модель користувача.

    Розширює стандартну Django-модель AbstractUser (рекомендований підхід
    для нових проєктів). Зберігає вхід за іменем користувача (username),
    але робить email обов'язковим та унікальним, додає поля профілю.
    """

    # Email обов'язковий і унікальний — потрібен для підтвердження реєстрації
    # та відновлення пароля.
    email = models.EmailField("Електронна пошта", unique=True)

    # Прапорець підтвердження email. Доки False — обліковий запис неактивний.
    email_confirmed = models.BooleanField("Email підтверджено", default=False)

    # Поля профілю, які користувач налаштовує після реєстрації.
    avatar = models.ImageField(
        "Аватар", upload_to="avatars/", blank=True, null=True
    )
    phone = models.CharField("Телефон", max_length=20, blank=True)
    address = models.CharField("Адреса доставки", max_length=255, blank=True)

    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"

    def __str__(self):
        return self.username
