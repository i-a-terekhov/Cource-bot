import asyncio
import logging
import sys
from os import getenv  # для запуска на https://replit.com
import tokenfile

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold


# TOKEN = getenv("BOT_TOKEN")  # для запуска на https://replit.com
TOKEN = tokenfile.token

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")
    await message.answer("Как твои дела?")


@dp.message()
async def how_are_you(message: Message) -> None:
    if message.text == "Ок":
        await message.answer(f"Хорошо!")
    else:
        await message.answer("Похоже, ты не ответил на мой вопрос.")


@dp.message()
async def echo_handler(message: types.Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
