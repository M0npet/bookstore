"""
REST API на Django REST Framework.

ListCreateAPIView надає методи GET (список) і POST (створення).
RetrieveUpdateDestroyAPIView надає GET (один об'єкт), PUT/PATCH (зміна),
DELETE (видалення). Таким чином реалізовано GET, POST і DELETE.
"""
from rest_framework import generics

from catalog.models import Book, Category
from .serializers import BookSerializer, CategorySerializer


class BookListCreateAPIView(generics.ListCreateAPIView):
    """GET — список книг (з пошуком), POST — додавання книги."""
    serializer_class = BookSerializer

    def get_queryset(self):
        qs = Book.objects.select_related("category").all()
        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(title__icontains=search)
        book_type = self.request.query_params.get("type")
        if book_type:
            qs = qs.filter(book_type=book_type)
        return qs


class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """GET — одна книга, PUT/PATCH — зміна, DELETE — видалення."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "pk"


class CategoryListAPIView(generics.ListAPIView):
    """GET — список категорій."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
