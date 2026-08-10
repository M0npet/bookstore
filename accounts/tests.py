"""Тести реєстрації та активації облікового запису."""
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token

User = get_user_model()


class RegistrationTests(TestCase):
    def test_register_creates_inactive_user_and_sends_email(self):
        """Після реєстрації користувач створюється неактивним, лист надсилається."""
        response = self.client.post(reverse("accounts:register"), {
            "username": "reader1",
            "email": "reader1@example.com",
            "password1": "SkladnyParol123",
            "password2": "SkladnyParol123",
        })
        self.assertEqual(response.status_code, 302)  # редірект на логін
        user = User.objects.get(username="reader1")
        self.assertFalse(user.is_active)            # ще не активований
        self.assertFalse(user.email_confirmed)
        self.assertEqual(len(mail.outbox), 1)       # лист активації надіслано

    def test_activation_link_activates_user(self):
        """Перехід за коректним посиланням активує користувача."""
        user = User.objects.create_user(
            username="reader2", email="reader2@example.com",
            password="SkladnyParol123", is_active=False,
        )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        response = self.client.get(
            reverse("accounts:activate", kwargs={"uidb64": uid, "token": token})
        )
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertTrue(user.email_confirmed)

    def test_duplicate_email_rejected(self):
        """Не можна зареєструвати двох користувачів з однаковим email."""
        User.objects.create_user(
            username="first", email="dup@example.com", password="SkladnyParol123"
        )
        response = self.client.post(reverse("accounts:register"), {
            "username": "second",
            "email": "dup@example.com",
            "password1": "SkladnyParol123",
            "password2": "SkladnyParol123",
        })
        self.assertEqual(response.status_code, 200)  # форма з помилкою
        self.assertFalse(User.objects.filter(username="second").exists())
