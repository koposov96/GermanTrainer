import random


from database.database import SessionLocal
from database.models import Word


def create_word(
        telegram_id: int,
        german: str,
        russian: str,
        category: str = "Общие слова",
        lesson: str = "Без категории"
):

    session = SessionLocal()

    word = Word(
        telegram_id=telegram_id,
        german=german,
        russian=russian,
        category=category,
        lesson=lesson
    )

    session.add(word)
    session.commit()
    session.close()


def get_random_word(telegram_id: int):

    session = SessionLocal()

    words = (
        session.query(Word)
        .filter(
            Word.telegram_id == telegram_id
        )
        .all()
    )

    session.close()

    if not words:
        return None

    return random.choice(words)

def get_all_words(telegram_id: int):

    session = SessionLocal()

    words = (
        session.query(Word)
        .filter(
            Word.telegram_id == telegram_id
        )
        .all()
    )

    session.close()

    return words

def get_categories(telegram_id: int):

    print("SEARCH CATEGORY FOR:", telegram_id)

    session = SessionLocal()

    categories = (
        session.query(Word.category)
        .filter(
            Word.telegram_id == telegram_id
        )
        .distinct()
        .all()
    )

    session.close()

    return [
        category[0]
        for category in categories
    ]