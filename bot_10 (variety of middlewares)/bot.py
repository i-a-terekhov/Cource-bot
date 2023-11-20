import asyncio
import logging

from aiogram import Bot, Dispatcher
from handlers import handler_alfa, handler_beta
from middlewares.middleware import Middleware

import tokenfile as tf


TOKEN = tf.TOKEN

bot_unit = Bot(token=TOKEN)


async def set_up_routers(dp):
    dp.include_routers(
        handler_beta.router,
        handler_alfa.router
    )

    # Несмотря на намеренно нелогичный порядок определения мидлварей ниже, вначале всегда выполняются outer:
    # Далее выполняются outer-middlewares из целевых роутеров, далее выполняются обычные middlewares
    dp.message.middleware(Middleware(middleware_name="Middleware_C"))
    dp.message.outer_middleware(Middleware(middleware_name="Middleware_A"))


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



