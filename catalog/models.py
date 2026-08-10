"""Моделі каталогу: категорії та книги."""
from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Категорія (жанр) книг."""

    name = models.CharField("Назва", max_length=100, unique=True)
    slug = models.SlugField("URL-ідентифікатор", max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            from .utils import ukr_slugify
            self.slug = ukr_slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:book_list_by_category", args=[self.slug])


class Book(models.Model):
    """
    Книга. Підтримує два типи:
      - друкована (PRINT): має запас на складі, доставляється поштою;
      - електронна (ELECTRONIC): має файл, завантажується після покупки.
    """

    class BookType(models.TextChoices):
        PRINT = "print", "Друкована"
        ELECTRONIC = "electronic", "Електронна"

    title = models.CharField("Назва", max_length=255)
    author = models.CharField("Автор", max_length=255)
    slug = models.SlugField("URL-ідентифікатор", max_length=255, unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name="Категорія",
        on_delete=models.PROTECT,
        related_name="books",
    )
    description = models.TextField("Опис", blank=True)
    price = models.DecimalField("Ціна, грн", max_digits=8, decimal_places=2)
    cover = models.ImageField(
        "Обкладинка", upload_to="covers/", blank=True, null=True
    )
    book_type = models.CharField(
        "Тип книги",
        max_length=20,
        choices=BookType.choices,
        default=BookType.PRINT,
    )

    # Тільки для друкованих: кількість на складі.
    stock = models.PositiveIntegerField("Запас на складі", default=0)

    # Тільки для електронних: файл для завантаження після покупки.
    digital_file = models.FileField(
        "Файл книги", upload_to="ebooks/", blank=True, null=True
    )

    available = models.BooleanField("Доступна для продажу", default=True)
    created_at = models.DateTimeField("Додано", auto_now_add=True)

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["book_type"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            from .utils import ukr_slugify
            base = ukr_slugify(f"{self.title}-{self.author}")
            slug = base
            counter = 1
            # Гарантуємо унікальність slug.
            while Book.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} — {self.author}"

    def get_absolute_url(self):
        return reverse("catalog:book_detail", args=[self.slug])

    @property
    def is_print(self):
        return self.book_type == self.BookType.PRINT

    @property
    def is_electronic(self):
        return self.book_type == self.BookType.ELECTRONIC

    @property
    def in_stock(self):
        """Чи можна купити: електронні — завжди, друковані — якщо є запас."""
        if self.is_electronic:
            return self.available
        return self.available and self.stock > 0
