"""Моделі замовлень."""
from django.conf import settings
from django.db import models


class Order(models.Model):
    """Замовлення користувача."""

    class Status(models.TextChoices):
        NEW = "new", "Нове"
        PAID = "paid", "Оплачено"
        SHIPPED = "shipped", "Відправлено"
        DONE = "done", "Виконано"
        CANCELLED = "cancelled", "Скасовано"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Користувач",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    # Контактні дані та адреса (адреса потрібна для друкованих книг — доставка поштою).
    full_name = models.CharField("Отримувач", max_length=255)
    email = models.EmailField("Email")
    phone = models.CharField("Телефон", max_length=20, blank=True)
    address = models.CharField("Адреса доставки", max_length=255, blank=True)

    needs_delivery = models.BooleanField("Потрібна доставка", default=False)
    status = models.CharField(
        "Статус", max_length=20, choices=Status.choices, default=Status.NEW
    )
    created_at = models.DateTimeField("Створено", auto_now_add=True)
    updated_at = models.DateTimeField("Оновлено", auto_now=True)

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Замовлення №{self.pk}"

    @property
    def total(self):
        """Загальна сума замовлення."""
        return sum(item.subtotal for item in self.items.all())


class OrderItem(models.Model):
    """Позиція замовлення (одна книга)."""

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items"
    )
    book = models.ForeignKey(
        "catalog.Book",
        verbose_name="Книга",
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    # Ціну фіксуємо на момент придбання — щоб подальша зміна ціни книги
    # не впливала на вже оформлені замовлення.
    price = models.DecimalField("Ціна", max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField("Кількість", default=1)

    class Meta:
        verbose_name = "Позиція замовлення"
        verbose_name_plural = "Позиції замовлення"

    def __str__(self):
        return f"{self.book} × {self.quantity}"

    @property
    def subtotal(self):
        return self.price * self.quantity
