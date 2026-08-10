"""
Налаштування проєкту "Інтернет-магазин книг".
Django 5.2 LTS.
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Безпека ---
# УВАГА: для робочого розгортання ключ слід зберігати в змінних оточення.
SECRET_KEY = "django-insecure-CHANGE-ME-IN-PRODUCTION-0123456789abcdef"
DEBUG = True
ALLOWED_HOSTS = ["*"]

# --- Застосунки ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Сторонні
    "rest_framework",
    # Власні застосунки
    "accounts",
    "catalog",
    "cart",
    "orders",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Власний: робить кошик доступним у всіх шаблонах
                "cart.context_processors.cart",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --- База даних ---
# SQLite — вбудована в Python, не потребує окремого сервера. Зручно для розробки.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --- Валідація паролів ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Локалізація ---
LANGUAGE_CODE = "uk"
TIME_ZONE = "Europe/Kyiv"
USE_I18N = True
USE_TZ = True

# --- Статика та медіа ---
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Власна модель користувача ---
AUTH_USER_MODEL = "accounts.User"

# --- Налаштування автентифікації ---
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "catalog:book_list"
LOGOUT_REDIRECT_URL = "catalog:book_list"

# --- Пошта ---
# Для розробки листи друкуються в консоль (термінал), реальний сервер не потрібен.
# Для робочого режиму нижче наведено приклад SMTP (закоментовано).
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "Книгарня <noreply@bookstore.local>"
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = "your_email@gmail.com"
# EMAIL_HOST_PASSWORD = "your_app_password"

# --- Кошик у сесії ---
CART_SESSION_ID = "cart"

# --- Django REST Framework ---
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 12,
}
