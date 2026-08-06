from aiogram import Router
from aiogram.types import Message

from services.word_service import get_all_words


router = Router()


@router.message(lambda message: message.text == "📋 Мои слова")
async def my_words_handler(message: Message):

    words = get_all_words(
        message.from_user.id
    )


    if not words:
        await message.answer(
            "📚 У тебя пока нет слов."
        )
        return


    text = "📚 Твои слова:\n\n"


    for index, word in enumerate(words, start=1):

        text += (
            f"{index}. "
            f"{word.german} — {word.russian}\n"
        )


    await message.answer(text)