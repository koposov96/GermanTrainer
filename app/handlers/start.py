from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main_menu import main_menu


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "🇩🇪 German Trainer\n\n"
        "Выбери действие:",
        reply_markup=main_menu
    )