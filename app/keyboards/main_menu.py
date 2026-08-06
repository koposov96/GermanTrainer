from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📚 Добавить слово"),
            KeyboardButton(text="🎯 Учить слова")
        ],
        [
            KeyboardButton(text="📋 Мои слова"),
            KeyboardButton(text="📊 Статистика")
        ]
    ],
    resize_keyboard=True
)