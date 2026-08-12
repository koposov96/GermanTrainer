import random

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.word_service import (
    get_random_word,
    get_random_word_by_lesson,
    get_random_difficult_word,
    set_word_difficult,
    get_categories,
    get_lessons
)

router = Router()


class Training(StatesGroup):
    answer = State()


def training_menu_keyboard():

    builder = InlineKeyboardBuilder()

    builder.button(
        text="📚 Все слова",
        callback_data="training:all"
    )

    builder.button(
        text="📂 По уроку",
        callback_data="training:lesson"
    )

    builder.button(
        text="⭐ Сложные слова",
        callback_data="training:difficult"
    )

    builder.adjust(1)

    return builder.as_markup()


def training_categories_keyboard(categories):

    builder = InlineKeyboardBuilder()

    for category in categories:

        builder.button(
            text=f"📁 {category}",
            callback_data=f"training_category:{category}"
        )

    builder.button(
        text="⬅️ Назад",
        callback_data="training:menu"
    )

    builder.adjust(1)

    return builder.as_markup()


def training_lessons_keyboard(category, lessons):

    builder = InlineKeyboardBuilder()

    for lesson in lessons:

        builder.button(
            text=f"📂 {lesson}",
            callback_data=f"training_lesson:{category}:{lesson}"
        )

    builder.button(
        text="⬅️ Назад",
        callback_data="training:lesson"
    )

    builder.adjust(1)

    return builder.as_markup()

def word_training_keyboard(word):
    builder = InlineKeyboardBuilder()

    if word.difficult:
        builder.button(
            text="⭐ Убрать из сложных",
            callback_data=f"word_difficult:remove:{word.id}"
        )
    else:
        builder.button(
            text="⭐ Добавить в сложные",
            callback_data=f"word_difficult:add:{word.id}"
        )

    builder.adjust(1)

    return builder.as_markup()

async def send_next_word(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()

    telegram_id = data["telegram_id"]

    training_mode = data.get(
        "training_mode",
        "all"
    )

    if training_mode == "lesson":

        category = data["category"]
        lesson = data["lesson"]

        word = get_random_word_by_lesson(
            telegram_id,
            category,
            lesson
        )

    elif training_mode == "difficult":

        word = get_random_difficult_word(
            telegram_id
        )

    else:

        word = get_random_word(
            telegram_id
        )

    if not word:

        await message.answer(
            "У тебя пока нет слов для обучения."
        )

        await state.clear()

        return

    direction = random.choice(
        ["de_ru", "ru_de"]
    )

    if direction == "de_ru":

        question = word.german
        correct = word.russian

        text = (
            f"🇩🇪 Переведи на русский:\n\n"
            f"{question}"
        )

    else:

        question = word.russian
        correct = word.german

        text = (
            f"🇷🇺 Переведи на немецкий:\n\n"
            f"{question}"
        )

    await state.update_data(
        correct=correct,
        word_id=word.id
    )

    await state.set_state(
        Training.answer
    )

    await message.answer(
        text,
        reply_markup=word_training_keyboard(word)
    )


@router.message(
    lambda message: message.text == "🎯 Учить слова"
)
async def start_training(
    message: Message,
    state: FSMContext
):

    print("USER ID:", message.from_user.id)
    print("USER NAME:", message.from_user.username)
    print("CHAT ID:", message.chat.id)

    await state.clear()

    await state.update_data(
        telegram_id=message.from_user.id
    )

    await message.answer(
        "🎯 Как будем учить слова?",
        reply_markup=training_menu_keyboard()
    )


@router.callback_query(
    lambda call: call.data == "training:all"
)
async def training_all(
    call: CallbackQuery,
    state: FSMContext
):

    await state.clear()

    await state.update_data(
        telegram_id=call.from_user.id,
        training_mode="all"
)

    await call.message.edit_text(
        "📚 Тренировка по всем словам началась!"
    )

    await send_next_word(
        call.message,
        state
    )

    await call.answer()

@router.callback_query(
    lambda call: call.data == "training:difficult"
)
async def training_difficult(
    call: CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await state.update_data(
        telegram_id=call.from_user.id,
        training_mode="difficult"
    )

    await call.message.edit_text(
        "⭐ Тренировка по сложным словам началась!"
    )

    await send_next_word(
        call.message,
        state
    )

    await call.answer()
    
@router.callback_query(
    lambda call: call.data == "training:lesson"
)
async def training_by_lesson(
    call: CallbackQuery,
    state: FSMContext
):

    categories = get_categories(
        call.from_user.id
    )

    if not categories:

        await call.message.edit_text(
            "У тебя пока нет слов."
        )

        await call.answer()

        return

    await call.message.edit_text(
        "📚 Выбери раздел:",
        reply_markup=training_categories_keyboard(
            categories
        )
    )

    await call.answer()


@router.callback_query(
    lambda call: call.data.startswith("training_category:")
)
async def training_category_selected(
    call: CallbackQuery,
    state: FSMContext
):

    category = call.data.split(
        ":",
        1
    )[1]

    lessons = get_lessons(
        call.from_user.id,
        category
    )

    await call.message.edit_text(
        f"📁 {category}\n\nВыбери урок:",
        reply_markup=training_lessons_keyboard(
            category,
            lessons
        )
    )

    await call.answer()


@router.callback_query(
    lambda call: call.data.startswith("training_lesson:")
)
async def training_lesson_selected(
    call: CallbackQuery,
    state: FSMContext
):

    parts = call.data.split(":")

    category = parts[1]
    lesson = ":".join(parts[2:])

    await state.clear()

    await state.update_data(
        telegram_id=call.from_user.id,
        training_mode="lesson",
        category=category,
        lesson=lesson
    )

    await call.message.edit_text(
        f"📂 Тренировка: {lesson}"
    )

    await send_next_word(
        call.message,
        state
    )

    await call.answer()


@router.callback_query(
    lambda call: call.data == "training:menu"
)
async def training_menu(
    call: CallbackQuery,
    state: FSMContext
):

    await state.clear()

    await call.message.edit_text(
        "🎯 Как будем учить слова?",
        reply_markup=training_menu_keyboard()
    )

    await call.answer()

@router.callback_query(
    lambda call: call.data.startswith("word_difficult:add:")
)
async def add_difficult_word(
    call: CallbackQuery,
    state: FSMContext
):

    word_id = int(
        call.data.split(":")[-1]
    )

    set_word_difficult(
        call.from_user.id,
        word_id,
        True
    )

    await call.answer(
        "✅ Добавлено в сложные слова"
    )

@router.callback_query(
    lambda call: call.data.startswith("word_difficult:remove:")
)
async def remove_difficult_word(
    call: CallbackQuery,
    state: FSMContext
):

    word_id = int(
        call.data.split(":")[-1]
    )

    set_word_difficult(
        call.from_user.id,
        word_id,
        False
    )

    await call.answer(
        "✅ Убрано из сложных слов"
    )

@router.message(
    Training.answer,
    lambda message: message.text not in [
        "📋 Мои слова",
        "🎯 Учить слова",
        "📊 Статистика"
    ]
)
async def check_answer(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()

    correct = data["correct"]

    # Допустимые варианты ответа из базы.
    # Например:
    # "звук, шум"
    # превращается в ["звук", "шум"]
    correct_variants = [
        variant.strip().lower()
        for variant in correct.split(",")
        if variant.strip()
    ]

    # Ответ пользователя.
    # Вводить варианты тоже нужно через запятую.
    user_variants = [
        variant.strip().lower()
        for variant in message.text.split(",")
        if variant.strip()
    ]

    # Сравниваем наборы без учета порядка.
    if all(
        variant in correct_variants
        for variant in user_variants
    ):

        await message.answer(
            "✅ Правильно!"
        )

    else:

        await message.answer(
            f"❌ Неправильно.\n\n"
            f"Правильный ответ:\n"
            f"{correct}"
        )

    await send_next_word(
        message,
        state
    )