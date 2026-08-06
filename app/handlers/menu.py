from aiogram import Router
from aiogram.types import Message


router = Router()


@router.message(lambda message: message.text in [
    "🎯 Учить слова",
    "📊 Статистика"
])
async def menu_handler(message: Message):

    if message.text == "🎯 Учить слова":
        await message.answer(
            "Режим обучения скоро будет"
        )

    elif message.text == "📊 Статистика":
        await message.answer(
            "Статистика скоро будет"
        )