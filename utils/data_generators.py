import random
import string
from datetime import datetime, timedelta, timezone

from faker import Faker

fake = Faker()


class DataGenerator:
    @staticmethod
    def random_email() -> str:
        return fake.email()

    @staticmethod
    def random_full_name() -> str:
        return fake.name()

    @staticmethod
    def random_password(min_len: int = 8, max_len: int = 16) -> str:
        length = random.randint(min_len, max_len)
        chars = (
            [random.choice(string.ascii_uppercase)]
            + [random.choice(string.ascii_lowercase)]
            + [random.choice(string.digits)]
            + [random.choice(string.ascii_letters + string.digits) for _ in range(length - 3)]
        )
        random.shuffle(chars)
        return "".join(chars)

    @staticmethod
    def random_sentence(nb_words: int = 6) -> str:
        return fake.sentence(nb_words=nb_words)

    @staticmethod
    def random_paragraph(nb_sentences: int = 3) -> str:
        return fake.paragraph(nb_sentences=nb_sentences)

    @staticmethod
    def future_datetime(hours_ahead: int = 24) -> str:
        """ISO 8601: now + N hours, rounded to hour."""
        future = datetime.now(timezone.utc) + timedelta(hours=hours_ahead)
        rounded = future.replace(minute=0, second=0, microsecond=0)
        return rounded.strftime("%Y-%m-%dT%H:%M:%S.000Z")
