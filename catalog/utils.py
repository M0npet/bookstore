"""Утиліти каталогу: транслітерація кирилиці для ЧПУ-адрес (slug)."""
from django.utils.text import slugify

# Спрощена таблиця транслітерації українська → латиниця.
UA_MAP = {
    "а": "a", "б": "b", "в": "v", "г": "h", "ґ": "g", "д": "d", "е": "e",
    "є": "ie", "ж": "zh", "з": "z", "и": "y", "і": "i", "ї": "i", "й": "i",
    "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r",
    "с": "s", "т": "t", "у": "u", "ф": "f", "х": "kh", "ц": "ts", "ч": "ch",
    "ш": "sh", "щ": "shch", "ь": "", "ю": "iu", "я": "ia", "'": "", "’": "",
}


def transliterate(text):
    """Перетворює український текст у латиницю за таблицею UA_MAP."""
    result = []
    for char in text.lower():
        result.append(UA_MAP.get(char, char))
    return "".join(result)


def ukr_slugify(text):
    """Створює ASCII-slug з українського тексту."""
    return slugify(transliterate(text))
