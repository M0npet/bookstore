"""Маршрути каталогу."""
from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.book_list, name="book_list"),
    path("category/<slug:category_slug>/", views.book_list, name="book_list_by_category"),
    path("book/<slug:slug>/", views.book_detail, name="book_detail"),
]
