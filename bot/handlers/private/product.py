from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import lazy_gettext as __
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from bot.buttons.inline import menu_btn, buy_now_button, counter_btn
from bot.buttons.reply import phone_button, SellerState, main_button
from bot.utils import caption_book
from db.models import Product, User

product_router = Router()
# SELLER_ID = '5030397655'


SELLER_ID = '7139720225'


# Menyu handler
@product_router.message(F.text == __('🍖🥗 Zakaz berish'))
async def books_handler(message: Message, session: Session) -> None:
    products: list[Product] = list(session.execute(select(Product)).scalars())
    await message.answer(".                          📋МЕНЮ\n\n", reply_markup=menu_btn(products))


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
async def buy_product(callback: CallbackQuery, state: FSMContext) -> None:
    product_id = callback.data.split("_")[1]  # `buy_` dan keyingi ID ni olish
    await state.update_data({"product_id": product_id})  # Holatda saqlash
    await state.set_state(SellerState.phone_number)
    await callback.message.answer("Iltimos, telefon raqamingizni yuboring!", reply_markup=await phone_button())


# Telefon raqamni qabul qilish va sotuvchiga ma'lumot jo'natish
@product_router.message(SellerState.phone_number, F.contact)
async def phone_number_handler(message: Message, session, state: FSMContext) -> None:
    await state.update_data({"phone_number": message.contact.phone_number})
    phone_number = message.contact.phone_number
    await state.update_data({"phone_number": phone_number})
    # `buy_` ni ajratib olish uchun ma'lumotni olish
    data = await state.get_data()
    product_id = int(data.get("product_id"))  # Mahsulot ID oldindan holatda saqlanadi

    # Mahsulotni bazadan olish
    _product = session.execute(select(Product).where(Product.id == product_id)).scalar()

    if not _product:
        await message.answer("Kechirasiz, ushbu mahsulot topilmadi.")
        await state.clear()
        return

    user = message.from_user
    counter = data.get("counter", 1)

    # Foydalanuvchi haqida ma'lumot
    user_info = (
        f"👤 Foydalanuvchi profili:\n"
        f"📛 Ismi: {user.full_name}\n"
        f"📱 Telefon: {phone_number}\n"
        f"🔗 Username: @{user.username}" if user.username else "🔗 Username: Mavjud emas"
    )

    # Sotuvchiga xabar tayyorlash
    message_to_seller = (
        f"🥘 Yangi zakaz!\n"
        f"🥗 Mahsulot: {_product.title}\n"
        f"🍽 Nechta: {counter} ta\n"
        f"📜 Ma'lumot: {_product.description}\n"
        f"💵 Narxi: {_product.price} so'm\n\n"
        f"{user_info}\n"
    )

    # Sotuvchiga xabar yuborish
    await message.bot.send_message(chat_id=SELLER_ID, text=message_to_seller)

    # Foydalanuvchiga tasdiq xabari
    await message.answer("✅ Zakazingiz qabul qilindi!")
    await message.answer("Haridingiz uchun rahmat, sizni do'konimizda kutib qolamiz 😉", reply_markup=main_button())
    await state.clear()


@product_router.message(F.text == __('👤 Do\'kon egasi b-n bog\'lanish'))
async def books_handler(message: Message, session: Session) -> None:
    await message.answer("t.me/ixlos_o63\n+998932889274")


@product_router.callback_query(F.data.startswith("question"))
async def Seller_profile(callback: CallbackQuery, session) -> None:
    await callback.message.answer("t.me/ixlos_o63\n+998932889274")


@product_router.callback_query(F.data.startswith("takeaway_"))
async def takeaway_handler(callback: CallbackQuery, session, state: FSMContext) -> None:
    # Mahsulot ID ni olish
    product_id = int(callback.data.split("_")[1])
    await state.update_data({"product_id": product_id})

    # Foydalanuvchidan telefon raqamini olish
    await state.set_state(SellerState.zakaz)
    await callback.message.answer(
        "Iltimos, telefon raqamingizni yuboring!",
        reply_markup=await phone_button()
    )


@product_router.message(SellerState.zakaz, F.contact)
async def phone_number_handler(message: Message, session, state: FSMContext) -> None:
    phone_number = message.contact.phone_number
    await state.update_data({"phone_number": phone_number})

    # Mahsulot ID ni holatdan olish
    data = await state.get_data()
    product_id = data.get("product_id")
    if not product_id:
        await message.answer("Mahsulot topilmadi. Iltimos, qaytadan urinib ko'ring.")
        await state.clear()
        return

    # Mahsulotni bazadan olish
    _product = session.execute(select(Product).where(Product.id == product_id)).scalar()
    if not _product:
        await message.answer("Kechirasiz, ushbu mahsulot topilmadi.")
        await state.clear()
        return

    # Foydalanuvchi haqida ma'lumot
    user = message.from_user
    counter = data.get("counter", 1)

    user_info = (
        f"👤 Foydalanuvchi profili:\n"
        f"📛 Ismi: {user.full_name}\n"
        f"📱 Telefon: {phone_number}\n"
        f"🔗 Username: @{user.username}" if user.username else "🔗 Username: Mavjud emas"
    )

    # Sotuvchiga yuboriladigan xabar
    message_to_seller = (
        f"🥘 Yangi zakaz!\n"
        f"🥗 Mahsulot: {_product.title}\n"
        f"🍽 Nechta: {counter} ta\n"
        f"📜 Ma'lumot: {_product.description}\n"
        f"💵 Narxi: {_product.price} so'm\n\n"
        f"{user_info}\n"
        f"❗️ ❗️ ❗️ САБОЙ ❗️ ❗️ ❗️"
    )

    # Sotuvchiga xabar yuborish
    await message.bot.send_message(chat_id=SELLER_ID, text=message_to_seller)

    # Foydalanuvchiga tasdiq xabari
    await message.answer("✅ Zakazingiz qabul qilindi!")
    await message.answer("Haridingiz uchun rahmat, sizni do'konimizda kutib qolamiz 😉", reply_markup=main_button())