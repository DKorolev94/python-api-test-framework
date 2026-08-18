from datetime import UTC, datetime, timedelta

from faker import Faker

fake = Faker()


def random_email() -> str:
    """Генерирует случайный email для тестовых данных."""
    return fake.email()


def random_full_name() -> str:
    """Генерирует случайное полное имя для тестовых данных."""
    return fake.name()


def random_sentence(nb_words: int = 6) -> str:
    """Генерирует случайное предложение для тестовых данных."""
    return fake.sentence(nb_words=nb_words)


def random_paragraph(nb_sentences: int = 3) -> str:
    """Генерирует случайный абзац текста для тестовых данных."""
    return fake.paragraph(nb_sentences=nb_sentences)


def future_datetime(hours_ahead: int = 24) -> str:
    """Возвращает текущее время плюс N часов в формате ISO 8601, округлённое до часа."""
    future = datetime.now(UTC) + timedelta(hours=hours_ahead)
    rounded = future.replace(minute=0, second=0, microsecond=0)
    return rounded.strftime("%Y-%m-%dT%H:%M:%S.000Z")
