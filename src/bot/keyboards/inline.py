from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.constans import ZODIAC_SIGNS_LITERALS
from bot.utils.helpers import get_sign_data


def get_inline_signs_keyboard():
    builder = InlineKeyboardBuilder()

    for key in ZODIAC_SIGNS_LITERALS:
        ru_sign, emoji = get_sign_data(key)
        builder.button(
            text=f"{ru_sign} {emoji}",
            callback_data=f"{key}",
        )

    return builder.adjust(3).as_markup()


schedule_subscribe_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Подписаться на гороскоп", callback_data="subscribe_horoscope"
            )
        ]
    ]
)

schedule_unsubscribe_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="❌ Отписаться от гороскопа", callback_data="unsubscribe_horoscope"
            )
        ]
    ]
)
