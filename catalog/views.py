"""В'юшки каталогу: список книг (з пошуком і фільтрами) та сторінка книги."""
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Book, Category


def book_list(request, category_slug=None):
    """Список книг із пошуком, фільтром за типом і категорією."""
    categories = Category.objects.all()
    books = Book.objects.filter(available=True).select_related("category")

    # Фільтр за категорією (через URL)
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        books = books.filter(category=category)

    # Пошук за назвою або автором
    query = request.GET.get("q", "").strip()
    if query:
        books = books.filter(title__icontains=query) | books.filter(
            author__icontains=query
        )

    # Фільтр за типом книги (друкована / електронна)
    book_type = request.GET.get("type", "")
    if book_type in (Book.BookType.PRINT, Book.BookType.ELECTRONIC):
        books = books.filter(book_type=book_type)

    # Розбиття на сторінки
    paginator = Paginator(books, 8)
    page = request.GET.get("page")
    books_page = paginator.get_page(page)

    return render(
        request,
        "catalog/book_list.html",
        {
            "categories": categories,
            "category": category,
            "books": books_page,
            "query": query,
            "selected_type": book_type,
        },
    )


def book_detail(request, slug):
    """Сторінка окремої книги."""
    book = get_object_or_404(Book, slug=slug, available=True)
    return render(request, "catalog/book_detail.html", {"book": book})
