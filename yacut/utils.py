import random
import string

from .models import URLMap


def get_unique_short_id(length=6):
    """Функция для генерации короткой ссылки."""

    chars = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choice(chars) for _ in range(length))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id
