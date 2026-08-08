from aiogram import Router
from fastapi import APIRouter

from services.word_service import import_words


router = APIRouter()


@router.post("/import")
def import_from_api(data: dict):

    added = import_words(
        telegram_id=data["telegram_id"],
        category=data["category"],
        lesson=data["lesson"],
        words=data["words"]
    )

    return {
        "status": "success",
        "added": added
    }