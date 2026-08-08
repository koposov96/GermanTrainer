import asyncio
import logging

from database.database import Base, engine
from database import models
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.start import router as start_router
from handlers.words import router as words_router
from handlers.training import router as training_router
from handlers.menu import router as menu_router
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.categories import router as categories_router
from handlers.import_words import router as import_router


logging.basicConfig(level=logging.INFO)


bot = Bot(token=BOT_TOKEN)

dp = Dispatcher(
    storage=MemoryStorage()
)


dp.include_router(start_router)
dp.include_router(import_router)
dp.include_router(words_router)
dp.include_router(training_router)
dp.include_router(categories_router)
dp.include_router(menu_router)

Base.metadata.create_all(engine)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())