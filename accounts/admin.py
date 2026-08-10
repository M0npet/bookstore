from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Адмін-панель користувача з додатковими полями профілю."""

    list_display = ("username", "email", "email_confirmed", "is_staff")
    list_filter = ("email_confirmed", "is_staff", "is_active")
    # Додаємо власні поля до стандартних наборів полів UserAdmin.
    fieldsets = UserAdmin.fieldsets + (
        ("Профіль", {"fields": ("email_confirmed", "avatar", "phone", "address")}),
    )
