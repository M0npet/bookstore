"""Тести REST API."""
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from catalog.models import Book, Category


class BookAPITests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="API-тест", slug="api-test")
        self.book = Book.objects.create(
            title="API книга", author="Автор", slug="api-book",
            category=self.category, price=Decimal("250.00"),
            book_type=Book.BookType.ELECTRONIC, available=True,
        )

    def test_get_book_list(self):
        """GET /api/books/ повертає список книг у JSON."""
        response = self.client.get(reverse("api:book_list"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["title"], "API книга")

    def test_get_single_book(self):
        """GET /api/books/<id>/ повертає одну книгу."""
        response = self.client.get(reverse("api:book_detail", args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["author"], "Автор")

    def test_search_books(self):
        """GET /api/books/?search= фільтрує за назвою."""
        response = self.client.get(reverse("api:book_list"), {"search": "неіснуюча"})
        self.assertEqual(response.json()["count"], 0)
