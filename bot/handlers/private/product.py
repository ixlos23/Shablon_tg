from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import lazy_gettext as __
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from bot.buttons.inline import menu_btn, buy_now_button, counter_btn
from bot.utils import caption_book
from db.models import Product, User

product_router = Router()
SELLER_ID = '5030397655'
# SELLER_ID = '7139720225'


# Menyu handler
@product_router.message(F.text == __('🍖🥗 Zakaz berish'))
async def books_handler(message: Message, session: Session) -> None:
    products: list[Product] = list(session.execute(select(Product)).scalars())
    await message.answer(".             📋МЕНЮ\n\n", reply_markup=menu_btn(products))


@product_router.callback_query(F.data.startswith('product_'))
async def product_handler(callback: CallbackQuery, session, state: FSMContext) -> None:
    value = callback.data.split('_')[1]
    if value.isdigit():  # Check if value is a valid number
        product_id = int(value)
        _product = session.execute(select(Product).where(Product.id == product_id)).scalar()
        counter = 0
        await state.update_data(counter=counter)
        if _product:
            await callback.message.answer_photo(
                photo=_product.photo,
                caption=caption_book(_product),
                reply_markup=counter_btn(counter),

            )
            await callback.message.answer("Zakaz berish uchun bosing👇", reply_markup=await buy_now_button(product_id))


@product_router.callback_query(F.data.startswith('counter_'))
async def counter_handler(callback: CallbackQuery, state: FSMContext) -> None:
    # Foydalanuvchi holati bo'yicha hisoblagichni olish
    data = await state.get_data()
    counter = data.get('counter')  # Holatdan qiymatni o'qish

    if counter is None:  # Agar qiymat hali holatda saqlanmagan bo'lsa
        counter = 1  # Default qiymatni 1 qilib belgilaymiz
        await state.update_data(counter=counter)  # Holatda saqlaymiz

    if 'increment' in callback.data:
        counter += 1  # Hisoblagichni oshirish
    elif 'decrement' in callback.data and counter > 1:  # 1 dan past bo'lishiga yo'l qo'ymaslik
        counter -= 1  # Hisoblagichni kamaytirish

    # Yangilangan hisoblagichni holatda saqlash
    await state.update_data(counter=counter)

    # Tugmalarni yangilangan hisoblagich bilan jo'natish
    await callback.message.edit_reply_markup(reply_markup=counter_btn(counter))


@product_router.callback_query(F.data.startswith("buy_"))
async def buy_product(callback: CallbackQuery, session, state: FSMContext) -> None:
    product_id = int(callback.data.split("_")[1])

    _product = session.execute(select(Product).where(Product.id == product_id)).scalar()

    # Callback handler for when the user sends their phone number

    if _product:
        user = callback.from_user
        user_record = session.execute(select(User).where(User.id == user.id)).scalar()
        phone_number = user_record.phone_number if user_record and user_record.phone_number else "Mavjud emas"
        data = await state.get_data()
        counter = data.get('counter', 1)
        user_info = (
            f"👤 Foydalanuvchi profili:\n"
            f"📛 Ismi: {user.full_name}\n"
            f"🔗 Username: @{user.username}" if user.username else "🔗 Username: Mavjud emas"
                                                                  f"\n📞 Telefon raqami: {phone_number}"
        )
        message_to_seller = (
            f"🥘 Yangi zakaz!\n"
            f"🥗 Mahsulot: {_product.title}\n"
            f"🍽 Nechta: {counter} ta\n"
            f"📜 Ma'lumot: {_product.description}\n"
            f"💵 Narxi: {_product.price} so'm\n"
            f"{user_info}\n"
            f"📞 Telefon raqami: {phone_number}"
        )
        await callback.bot.send_message(chat_id=SELLER_ID, text=message_to_seller)
        await callback.answer("Buyurtma qabul qilindi, sotuvchi bilan bog'lanishingiz mumkin.")
    else:
        await callback.answer("Kechirasiz, mahsulot topilmadi.")
    await callback.message.answer("✅ Zakazingiz qabul qilindi!")
    await callback.message.answer("Haridingiz uchun rahmat, sizni Do'konimizda kutib qolamiz 😉", show_alert=True)


@product_router.message(F.text == __('👤 Do\'kon egasi b-n bog\'lanish'))
async def books_handler(message: Message, session: Session) -> None:
    await message.answer("t.me/ixlos_o63\n+998932889274")


@product_router.callback_query(F.data.startswith("question"))
async def Seller_profile(callback: CallbackQuery, session) -> None:
    await callback.message.answer("t.me/ixlos_o63\n+998932889274")

'''
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/ixlos23/Baynal_market.git
git push -u origin main
'''