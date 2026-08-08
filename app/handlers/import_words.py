import json

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states.import_state import ImportState


router = Router()


@router.message(Command("import"))
async def import_command(
    message: Message,
    state: FSMContext
):
    await state.set_state(
        ImportState.waiting_json
    )

    await message.answer(
        "📥 Пришли JSON со словами."
    )

from services.word_service import import_words


@router.message(ImportState.waiting_json)
async def receive_json(
    message: Message,
    state: FSMContext
):

    try:

        data = json.loads(
            message.text
        )

    except json.JSONDecodeError:

        await message.answer(
            "❌ Неверный JSON."
        )

        return


    added = import_words(

        telegram_id=message.from_user.id,

        category=data["category"],

        lesson=data["lesson"],

        words=data["words"]

    )


    await state.clear()


    await message.answer(

        f"""✅ Импорт завершен

📺 {data["category"]}

📂 {data["lesson"]}

Добавлено слов: {added}"""

    )