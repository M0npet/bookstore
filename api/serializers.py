"""Серіалізатори DRF: перетворюють моделі у JSON і назад."""
from rest_framework import serializers

from catalog.models import Book, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class BookSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="name", queryset=Category.objects.all()
    )

    class Meta:
        model = Book
        fields = [
            "id", "title", "author", "slug", "category",
            "description", "price", "book_type", "stock", "available",
        ]
