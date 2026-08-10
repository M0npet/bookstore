"""Контекст-процесор: робить кошик доступним у будь-якому шаблоні як {{ cart }}."""
from .cart import Cart


def cart(request):
    return {"cart": Cart(request)}
