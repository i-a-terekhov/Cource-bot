import asyncio
import logging

from aiogram import Bot, Dispatcher

from handlers import questions, different_types
import tokenfile as tf

TOKEN = tf.TOKEN
bot_unit = Bot(token=TOKEN)


async def main(bot: Bot):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher()
    dp.include_routers(
        questions.router,
        different_types.router
    )

    # пропустить необработанные апдейты:
    # await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main(bot_unit))



