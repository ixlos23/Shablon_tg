from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, BotCommand
from aiogram.utils.i18n import gettext as _
from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from db.models import User

main_router = Router()


@main_router.message(CommandStart())
async def command_start_handler(message: Message, session: Session) -> None:
    is_exists = session.execute(select(User).where(User.user_id == message.from_user.id)).scalar()
    if not is_exists:
        user = {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "full_name": message.from_user.full_name
        }
        session.execute(insert(User).values(**user))
        session.commit()
    await message.answer(text="{} {}!".format(_('Hello'), message.from_user.full_name))
    await message.bot.set_my_commands(commands=[BotCommand(command='/start', description='Qayta ishga tushirish!')])