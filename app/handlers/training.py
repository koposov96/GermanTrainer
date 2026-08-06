import random

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from services.word_service import get_random_word


router = Router()


class Training(StatesGroup):
    answer = State()


@router.message(lambda message: message.text == "🎯 Учить слова")
async def start_training(
        message: Message,
        state: FSMContext
):

    word = get_random_word(
        message.from_user.id
    )

    if not word:
        await message.answer(
            "У тебя пока нет слов для обучения."
        )
        return


    direction = random.choice(
        ["de_ru", "ru_de"]
    )


    if direction == "de_ru":

        question = word.german
        correct = word.russian

        await message.answer(
            f"🇩🇪 Переведи на русский:\n\n"
            f"{question}"
        )


    else:

        question = word.russian
        correct = word.german

        await message.answer(
            f"🇷🇺 Переведи на немецкий:\n\n"
            f"{question}"
        )


    await state.update_data(
        correct=correct
    )


    await state.set_state(
        Training.answer
    )



@router.message(Training.answer)
async def check_answer(
        message: Message,
        state: FSMContext
):

    data = await state.get_data()

    correct = data["correct"]


    if message.text.lower().strip() == correct.lower().strip():

        await message.answer(
            "✅ Правильно!"
        )

    else:

        await message.answer(
            f"❌ Неправильно.\n\n"
            f"Правильный ответ:\n"
            f"{correct}"
        )


    await state.clear()