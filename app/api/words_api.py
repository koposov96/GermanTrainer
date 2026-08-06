from services.word_service import create_word


def add_word_from_api(
        telegram_id: int,
        german: str,
        russian: str,
        category: str,
        lesson: str
):

    create_word(
        telegram_id,
        german,
        russian,
        category,
        lesson
    )

    return {
        "status": "success",
        "word": german
    }