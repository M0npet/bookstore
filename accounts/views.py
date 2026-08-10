"""В'юшки реєстрації, активації та профілю."""
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import ProfileForm, RegisterForm
from .models import User
from .tokens import account_activation_token


def register(request):
    """Реєстрація користувача з підтвердженням email."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Доки email не підтверджено — обліковий запис неактивний,
            # увійти не можна.
            user.is_active = False
            user.save()
            _send_activation_email(request, user)
            messages.success(
                request,
                "Реєстрація майже завершена! Перевірте пошту та перейдіть "
                "за посиланням для активації облікового запису.",
            )
            return redirect("accounts:login")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def _send_activation_email(request, user):
    """Формує і надсилає лист з посиланням активації."""
    context = {
        "user": user,
        "domain": request.get_host(),
        "scheme": "https" if request.is_secure() else "http",
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": account_activation_token.make_token(user),
    }
    subject = "Активація облікового запису — Книгарня"
    body = render_to_string("accounts/activation_email.html", context)
    user.email_user(subject, body)


def activate(request, uidb64, token):
    """Обробка переходу за посиланням активації з листа."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        messages.success(request, "Email підтверджено. Ласкаво просимо!")
        return redirect("catalog:book_list")

    messages.error(request, "Посилання активації недійсне або застаріле.")
    return render(request, "accounts/activation_invalid.html")


@login_required
def profile(request):
    """Перегляд та редагування профілю + історія замовлень."""
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профіль оновлено.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=request.user)

    orders = request.user.orders.all()
    return render(
        request, "accounts/profile.html", {"form": form, "orders": orders}
    )
