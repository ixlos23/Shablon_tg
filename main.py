import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import FSMI18nMiddleware, I18n

from bot.dispatcher import TOKEN
from bot.handlers import dp
from db.config import engine
from db.models import Base
from utils.middlewares import CustomMiddleware

i18n = I18n(path='locales')


def on_startup():
    Base.metadata.create_all(engine)


async def register_all_middleware():
    dp.update.middleware(CustomMiddleware())
    dp.update.middleware(FSMI18nMiddleware(i18n=i18n))


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await register_all_middleware()
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

