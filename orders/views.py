"""В'юшки замовлень: оформлення, перегляд, завантаження е-книг."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart
from catalog.models import Book
from .forms import OrderCreateForm
from .models import Order, OrderItem


@login_required
def order_create(request):
    """Оформлення замовлення з вмісту кошика."""
    cart = Cart(request)
    items = list(cart)
    if not items:
        messages.info(request, "Ваш кошик порожній.")
        return redirect("catalog:book_list")

    needs_delivery = cart.has_printed_items()

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Якщо є друковані книги — адреса обов'язкова.
            if needs_delivery and not form.cleaned_data.get("address"):
                form.add_error("address", "Вкажіть адресу для доставки друкованих книг.")
            else:
                order = form.save(commit=False)
                order.user = request.user
                order.needs_delivery = needs_delivery
                order.save()
                # Переносимо позиції з кошика в замовлення.
                for item in items:
                    book = item["book"]
                    OrderItem.objects.create(
                        order=order,
                        book=book,
                        price=item["price"],
                        quantity=item["quantity"],
                    )
                    # Зменшуємо запас друкованих книг.
                    if book.is_print:
                        book.stock = max(book.stock - item["quantity"], 0)
                        book.save(update_fields=["stock"])
                cart.clear()
                messages.success(request, f"Замовлення №{order.pk} оформлено!")
                return redirect("orders:order_detail", order_id=order.pk)
    else:
        # Підставляємо дані з профілю користувача.
        form = OrderCreateForm(initial={
            "full_name": request.user.get_full_name() or request.user.username,
            "email": request.user.email,
            "phone": request.user.phone,
            "address": request.user.address,
        })

    return render(request, "orders/order_create.html", {
        "cart": cart, "items": items, "form": form, "needs_delivery": needs_delivery,
    })


@login_required
def order_detail(request, order_id):
    """Сторінка замовлення (доступна лише власнику)."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})


@login_required
def download_ebook(request, book_id):
    """
    Завантаження файлу електронної книги.
    Доступне лише якщо користувач купив цю книгу (має замовлення з нею).
    """
    book = get_object_or_404(Book, id=book_id, book_type=Book.BookType.ELECTRONIC)

    purchased = OrderItem.objects.filter(
        order__user=request.user, book=book
    ).exists()
    if not purchased:
        messages.error(request, "Ви ще не придбали цю книгу.")
        return redirect("catalog:book_detail", slug=book.slug)

    if not book.digital_file:
        raise Http404("Файл книги відсутній.")

    return FileResponse(
        book.digital_file.open("rb"), as_attachment=True,
        filename=f"{book.slug}{book.digital_file.name[book.digital_file.name.rfind('.'):]}",
    )
