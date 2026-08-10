"""Маршрути API."""
from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path("books/", views.BookListCreateAPIView.as_view(), name="book_list"),
    path("books/<int:pk>/", views.BookDetailAPIView.as_view(), name="book_detail"),
    path("categories/", views.CategoryListAPIView.as_view(), name="category_list"),
]
