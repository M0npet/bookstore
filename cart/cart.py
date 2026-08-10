"""
Кошик на основі сесії.

Дані кошика зберігаються в сесії користувача. Завдяки цьому кошик працює
і для незареєстрованих (гостей), і зберігається між візитами: сесія живе
у cookie та в базі сесій Django, тож після закриття вкладки й повернення
вміст кошика відновлюється.
"""
from decimal import Decimal

from django.conf import settings

from catalog.models import Book


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if cart is None:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # Повідомлення про товари, видалені як неактуальні (для показу користувачу).
        self.removed_messages = []

    def add(self, book, quantity=1, update_quantity=False):
        """Додати книгу або змінити її кількість."""
        book_id = str(book.id)
        if book_id not in self.cart:
            self.cart[book_id] = {"quantity": 0, "price": str(book.price)}

        if update_quantity:
            self.cart[book_id]["quantity"] = quantity
        else:
            self.cart[book_id]["quantity"] += quantity

        # Електронну книгу не має сенсу купувати більш ніж в 1 екземплярі.
        if book.is_electronic:
            self.cart[book_id]["quantity"] = 1
        # Для друкованої не даємо замовити більше, ніж є на складі.
        elif self.cart[book_id]["quantity"] > book.stock:
            self.cart[book_id]["quantity"] = max(book.stock, 1)

        self.save()

    def remove(self, book):
        """Видалити книгу з кошика."""
        book_id = str(book.id)
        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def _sync_availability(self):
        """
        Перевіряє актуальність позицій. Якщо книга стала недоступною
        (знята з продажу, видалена, або для друкованої скінчився запас) —
        видаляє її з кошика та готує повідомлення для користувача.
        Викликається під час перегляду кошика.
        """
        book_ids = list(self.cart.keys())
        existing = {
            str(b.id): b
            for b in Book.objects.filter(id__in=book_ids)
        }
        changed = False
        for book_id in book_ids:
            book = existing.get(book_id)
            if book is None or not book.available or (
                book.is_print and book.stock == 0
            ):
                title = book.title if book else "Книга"
                self.removed_messages.append(
                    f"«{title}» більше недоступна та була вилучена з кошика."
                )
                del self.cart[book_id]
                changed = True
        if changed:
            self.save()

    def __iter__(self):
        """Перебір позицій кошика з підвантаженням об'єктів книг."""
        self._sync_availability()
        book_ids = self.cart.keys()
        books = Book.objects.filter(id__in=book_ids)
        cart = self.cart.copy()
        for book in books:
            cart[str(book.id)]["book"] = book

        for item in cart.values():
            if "book" not in item:
                continue
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """Загальна кількість одиниць товару в кошику."""
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """Загальна сума до сплати."""
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    def has_printed_items(self):
        """Чи є в кошику друковані книги (тоді потрібна доставка)."""
        book_ids = self.cart.keys()
        return Book.objects.filter(
            id__in=book_ids, book_type=Book.BookType.PRINT
        ).exists()
