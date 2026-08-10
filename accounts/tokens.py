"""
Генератор токенів для підтвердження email.

Успадковуємо стандартний PasswordResetTokenGenerator: він уже вміє
створювати криптографічно стійкі токени, прив'язані до користувача й часу.
Додаємо до хешу поле email_confirmed — щойно email підтверджено, старі
посилання автоматично стають недійсними.
"""
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.email_confirmed}{user.is_active}"


account_activation_token = AccountActivationTokenGenerator()
