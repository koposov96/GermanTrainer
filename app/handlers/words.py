from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from services.word_service import create_word

print("WORDS HANDLER LOADED")


router = Router()


class AddWord(StatesGroup):
    german = State()
    russian = State()


@router.message(lambda message: message.text == "📚 Добавить слово")
async def add_word_start(message: Message, state: FSMContext):

    await message.answer(
        "Введите немецкое слово:"
    )

    await state.set_state(AddWord.german)


@router.message(AddWord.german)
async def get_german(
        message: Message,
        state: FSMContext
):

    await state.update_data(
        german=message.text
    )

    await message.answer(
        "Введите перевод:"
    )

    await state.set_state(AddWord.russian)


@router.message(AddWord.russian)
async def get_russian(
        message: Message,
        state: FSMContext
):

    data = await state.get_data()

    german = data["german"]
    russian = message.text

    create_word(
        message.from_user.id,
        german,
        russian,
        "Общие слова",
        "Без категории"
    )

    await message.answer(
        f"✅ Слово сохранено:\n\n"
        f"{german} — {russian}"
    )

    await state.clear()