from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import Product


# async def menu_btn(product_id):
#     design1 = [
#         [
#             InlineKeyboardButton(text="Фитчи", callback_data="fitchi_"),
#             InlineKeyboardButton(text="Патир", callback_data="patir_"),
#         ],
#         [
#             InlineKeyboardButton(text="Сомса", callback_data="somsa_"),
#             InlineKeyboardButton(text="Товуқ", callback_data="tovuq_"),
#         ],
#         [
#             InlineKeyboardButton(text="Салат", callback_data="salat_"),
#             InlineKeyboardButton(text="...", callback_data="empty_"),
#         ]
#     ]
#     return InlineKeyboardMarkup(inline_keyboard=design1)
#

async def buy_now_button(product_id):
    design1 = [
        InlineKeyboardButton(text='🤤🧆🍗 Zakaz berish!', callback_data=f"buy_{product_id}"),
        InlineKeyboardButton(text='💬 Sotuvchiga savol berish', callback_data="question"),
    ]
    design2 = [
        InlineKeyboardButton(text='🚗 O\'zi bilan olib ketish', callback_data=f"takeaway_{product_id}"),
    ]
    return InlineKeyboardMarkup(inline_keyboard=[design1, design2])


def menu_btn(products: list[Product]):
    ikb = InlineKeyboardBuilder()
    btns = [
        InlineKeyboardButton(text=product.title, callback_data=f"product_{product.id}") for product in products
    ]
    ikb.add(*btns)
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()


def counter_btn(counter: int) -> InlineKeyboardMarkup:
    """
    Hisoblagich tugmalarini yaratish.
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="-", callback_data="counter_decrement"),
            InlineKeyboardButton(text=f"{counter} ta", callback_data="counter_noop"),
            InlineKeyboardButton(text="+", callback_data="counter_increment"),
        ]
    ])
    return keyboard
