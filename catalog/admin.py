from django.contrib import admin
from .models import Category, Book


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "book_type", "price", "stock", "available")
    list_filter = ("book_type", "available", "category")
    search_fields = ("title", "author")
    list_editable = ("price", "stock", "available")
