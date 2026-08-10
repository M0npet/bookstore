"""Тести кошика."""
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from catalog.models import Book, Category


class CartTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Тест", slug="test")
        self.book = Book.objects.create(
            title="Тестова книга", author="Автор", slug="test-book",
            category=self.category, price=Decimal("100.00"),
            book_type=Book.BookType.PRINT, stock=5, available=True,
        )

    def test_add_to_cart(self):
        """Книга додається до кошика і зберігається в сесії."""
        response = self.client.post(
            reverse("cart:cart_add", args=[self.book.id]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        cart = self.client.session["cart"]
        self.assertIn(str(self.book.id), cart)
        self.assertEqual(cart[str(self.book.id)]["quantity"], 1)

    def test_guest_cart_persists_in_session(self):
        """Кошик гостя зберігається між запитами (через сесію)."""
        self.client.post(reverse("cart:cart_add", args=[self.book.id]))
        # Новий запит — сесія та сама, кошик на місці.
        response = self.client.get(reverse("cart:cart_detail"))
        self.assertContains(response, self.book.title)

    def test_remove_from_cart(self):
        """Книга видаляється з кошика."""
        self.client.post(reverse("cart:cart_add", args=[self.book.id]))
        self.client.post(reverse("cart:cart_remove", args=[self.book.id]))
        cart = self.client.session.get("cart", {})
        self.assertNotIn(str(self.book.id), cart)

    def test_unavailable_book_removed_from_cart(self):
        """Якщо книга стала недоступною — вона вилучається при перегляді кошика."""
        self.client.post(reverse("cart:cart_add", args=[self.book.id]))
        self.book.available = False
        self.book.save()
        response = self.client.get(reverse("cart:cart_detail"))
        cart = self.client.session.get("cart", {})
        self.assertNotIn(str(self.book.id), cart)
        self.assertContains(response, "недоступна")
