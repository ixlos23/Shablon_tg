from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.i18n import gettext as _


def main_button():
    design = [
        [
            KeyboardButton(text=_('🍖🥗 Zakaz berish')),
            KeyboardButton(text=_('👤 Do\'kon egasi b-n bog\'lanish'))
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
