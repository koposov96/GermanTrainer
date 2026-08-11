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

def get_random_word_by_lesson(
    telegram_id: int,
    category: str,
    lesson: str
):

    print("=== TRAINING SEARCH ===")
    print("telegram_id:", telegram_id)
    print("category:", repr(category))
    print("lesson:", repr(lesson))

    session = SessionLocal()

    available_lessons = (
        session.query(Word.lesson)
        .filter(
            Word.telegram_id == telegram_id,
            Word.category == category
        )
        .distinct()
        .all()
    )

    print(
        "LESSONS IN DB:",
        [repr(x[0]) for x in available_lessons]
    )

    words = (
        session.query(Word)
        .filter(
            Word.telegram_id == telegram_id,
            Word.category == category,
            Word.lesson == lesson
        )
        .all()
    )

    print("FOUND WORDS:", len(words))

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

def get_lessons(telegram_id: int, category: str):

    session = SessionLocal()

    lessons = (
        session.query(Word.lesson)
        .filter(
            Word.telegram_id == telegram_id,
            Word.category == category
        )
        .distinct()
        .all()
    )

    session.close()

    return [lesson[0] for lesson in lessons]

def get_words_by_lesson(
    telegram_id: int,
    category: str,
    lesson: str
):

    session = SessionLocal()

    words = (
        session.query(Word)
        .filter(
            Word.telegram_id == telegram_id,
            Word.category == category,
            Word.lesson == lesson
        )
        .order_by(Word.id)
        .all()
    )

    session.close()

    return words

def import_words(
    telegram_id: int,
    category: str,
    lesson: str,
    words: list
):

    session = SessionLocal()

    added = 0

    for item in words:

        exists = (
            session.query(Word)
            .filter(
                Word.telegram_id == telegram_id,
                Word.category == category,
                Word.lesson == lesson,
                Word.german == item["german"]
            )
            .first()
        )

        if exists:
            continue

        word = Word(
            telegram_id=telegram_id,
            german=item["german"],
            russian=item["russian"],
            category=category,
            lesson=lesson
        )

        session.add(word)
        added += 1

    session.commit()
    session.close()

    return added