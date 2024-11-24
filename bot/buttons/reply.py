from aiogram.fsm.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_button():
    design = [
        [
            KeyboardButton(text=_('🍖🥗 Zakaz berish')),
            KeyboardButton(text=_('👤 Do\'kon egasi b-n bog\'lanish'))
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def phone_button():
    rkm = ReplyKeyboardBuilder()
    rkm.add(*[KeyboardButton(text="tel.nomer qoldirish", request_contact=True)])
    rkm = rkm.as_markup(resize_keyboard=True)
    return rkm


class SellerState(StatesGroup):
    zakaz = State()
    phone_number = State()
