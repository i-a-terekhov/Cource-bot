import asyncio
import logging

from aiogram import Bot, Dispatcher
from handlers import checkin
from middlewares.weekend import WeekendCallbackMiddleware, WeekendMessageMiddleware
from middlewares.long_operation import ChatActionMiddleware

import tokenfile as tf

TOKEN = tf.TOKEN

bot_unit = Bot(token=TOKEN)


async def set_up_routers(dp):
    dp.include_routers(checkin.router)
    dp.message.outer_middleware(WeekendMessageMiddleware())
    dp.callback_query.outer_middleware(WeekendCallbackMiddleware())


async def main(bot: Bot):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher()
    await set_up_routers(dp)

    # пропустить необработанные апдейты:
    # await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main(bot_unit))



