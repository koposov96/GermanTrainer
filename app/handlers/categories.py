from aiogram import Router
from aiogram.types import Message, CallbackQuery

from services.word_service import get_categories
from keyboards.categories import categories_keyboard

from services.word_service import get_lessons
from keyboards.lessons import lessons_keyboard

from services.word_service import get_words_by_lesson


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

    lessons = get_lessons(
    call.from_user.id,
    category
)

    await call.message.edit_text(
    f"📁 {category}",
    reply_markup=lessons_keyboard(
        category,
        lessons
    )
)

    await call.answer()

@router.callback_query(lambda c: c.data == "back:categories")
async def back_to_categories(call: CallbackQuery):

    categories = get_categories(call.from_user.id)

    await call.message.edit_text(
        "📚 Выбери раздел:",
        reply_markup=categories_keyboard(categories)
    )

    await call.answer()

@router.callback_query(
    lambda call: call.data.startswith("lesson|")
)
async def lesson_selected(call: CallbackQuery):

    print("LESSON CLICKED")
    print(call.data)
    print(call.data.split(":"))

    _, category, lesson = call.data.split("|")

    words = get_words_by_lesson(
        call.from_user.id,
        category,
        lesson
    )

    text = f"📂 {lesson}\n\n"

    if not words:
        text += "Пока нет слов."
    else:
        for word in words:
            text += f"🇩🇪 {word.german} — 🇷🇺 {word.russian}\n"

    await call.message.edit_text(text)

    await call.answer()