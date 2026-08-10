"""Маршрути замовлень."""
from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("create/", views.order_create, name="order_create"),
    path("<int:order_id>/", views.order_detail, name="order_detail"),
    path("download/<int:book_id>/", views.download_ebook, name="download_ebook"),
]
