import asyncio

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message

from middlewares.slowpoke import SlowpokeMiddleware
import tokenfile as tf


TOKEN = tf.TOKEN
OWNER_CHAT_ID = tf.OWNER_CHAT_ID

bot_unit = Bot(token=TOKEN)
delay = 5  # second

router1 = Router()
router1.message.middleware(SlowpokeMiddleware(sleep_sec=delay))


@router1.message(F.text)
async def message_with_usernames(message: Message):
    await message.reply(text=f'А вот и мой ответ! Задержка составила {delay} секунд!')


async def main(bot: Bot):
    dp = Dispatcher()
    dp.include_routers(router1)

    await bot.send_message(chat_id=OWNER_CHAT_ID, text=f'Напиши мне текст, и я отвечу с задержкой в {delay} секунд!')

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main(bot_unit))



