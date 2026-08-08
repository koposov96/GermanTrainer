from aiogram.utils.keyboard import InlineKeyboardBuilder


def lessons_keyboard(category, lessons):

    builder = InlineKeyboardBuilder()

    for lesson in lessons:
        builder.button(
            text=f"📂 {lesson}",
            callback_data=f"lesson|{category}|{lesson}"
        )

    builder.button(
        text="⬅️ Назад",
        callback_data="back:categories"
    )

    builder.adjust(1)

    return builder.as_markup()