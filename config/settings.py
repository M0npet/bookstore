"""
Налаштування проєкту "Інтернет-магазин книг".
Django 5.2 LTS.
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Безпека ---
# Значення беруться зі змінних оточення. Це дозволяє використовувати ті самі
# файли і локально (режим розробки), і на хостингу (робочий режим),
# не зберігаючи секретний ключ у відкритому вигляді в коді.
import os

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-local-development-key-0123456789abcdef",
)

# DEBUG вмикається лише якщо явно задано DJANGO_DEBUG=True.
# На хостингу цю змінну не задають — отже, DEBUG вимкнено (вимога безпеки).
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

# Домени, з яких дозволено обслуговувати сайт.
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
_extra_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", "")
if _extra_hosts:
    ALLOWED_HOSTS += [h.strip() for h in _extra_hosts.split(",") if h.strip()]

# Довірені джерела для CSRF (потрібно для HTTPS-домену хостингу).
CSRF_TRUSTED_ORIGINS = [
    f"https://{h}" for h in ALLOWED_HOSTS if h not in ("127.0.0.1", "localhost")
]

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


# --- Додаткові налаштування безпеки для робочого режиму ---
# Вмикаються автоматично, коли DEBUG вимкнено (тобто на хостингу).
if not DEBUG:
    # Cookie передаються лише через захищене з'єднання HTTPS.
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # Захист від визначення типу вмісту браузером (MIME-sniffing).
    SECURE_CONTENT_TYPE_NOSNIFF = True
    # Заборона відображення сайту в чужому фреймі (захист від clickjacking).
    X_FRAME_OPTIONS = "DENY"
    # Примусове перенаправлення всіх запитів на HTTPS.
    SECURE_SSL_REDIRECT = True
    # HSTS: браузер запам'ятовує, що сайт доступний лише через HTTPS.
    SECURE_HSTS_SECONDS = 31536000  # 1 рік
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
