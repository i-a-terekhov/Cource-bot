import asyncio
import logging

from aiogram import Bot, Dispatcher
from handlers import handler_alfa
from middlewares.middleware_a import MiddlewareNoA


import tokenfile as tf

'''
уотер-мидлварь: в 20% случаях просто дропает апдейт, в остальных передает случайное число в апдейт
фильтр: в 25% случаях бракует апдейт на основании случайного числа
мидлварь: в 33% случаях сообщает о поломке бота

'''

TOKEN = tf.TOKEN

bot_unit = Bot(token=TOKEN)


async def set_up_routers(dp):
    dp.include_routers(handler_alfa.router)
    dp.message.outer_middleware(MiddlewareNoA())


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



