"""В'юшки кошика: додавання, зміна кількості, видалення, перегляд."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalog.models import Book
from .cart import Cart


@require_POST
def cart_add(request, book_id):
    """Додати книгу до кошика."""
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id, available=True)
    if not book.in_stock:
        messages.error(request, "На жаль, книги немає в наявності.")
        return redirect(book.get_absolute_url())
    cart.add(book=book)
    messages.success(request, f"«{book.title}» додано до кошика.")
    return redirect("cart:cart_detail")


@require_POST
def cart_update(request, book_id):
    """Змінити кількість позиції в кошику."""
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1
    if quantity < 1:
        cart.remove(book)
    else:
        cart.add(book=book, quantity=quantity, update_quantity=True)
    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, book_id):
    """Видалити позицію з кошика."""
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    messages.info(request, f"«{book.title}» вилучено з кошика.")
    return redirect("cart:cart_detail")


def cart_detail(request):
    """Перегляд кошика. Тут же спрацьовує перевірка актуальності позицій."""
    cart = Cart(request)
    items = list(cart)  # запускає _sync_availability()
    # Показуємо повідомлення про вилучені неактуальні позиції.
    for msg in cart.removed_messages:
        messages.warning(request, msg)
    return render(request, "cart/cart_detail.html", {"cart": cart, "items": items})
