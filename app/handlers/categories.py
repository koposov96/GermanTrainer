from aiogram import Router
from aiogram.types import Message, CallbackQuery

from services.word_service import get_categories
from keyboards.categories import categories_keyboard


router = Router()


@router.message(lambda message: message.text == "📋 Мои слова")
async def categories_handler(
        message: Message
):

    categories = get_categories(
        message.from_user.id
    )


    if not categories:
        await message.answer(
            "📚 У тебя пока нет слов."
        )
        return


    await message.answer(
        "📚 Выбери раздел:",
        reply_markup=categories_keyboard(categories)
    )


@router.callback_query(
    lambda call: call.data.startswith("category:")
)
async def category_selected(
        call: CallbackQuery
):

    category = call.data.split(":")[1]

    await call.message.answer(
        f"📁 Раздел:\n\n{category}\n\n"
        "Здесь позже будут уроки."
    )

    await call.answer()