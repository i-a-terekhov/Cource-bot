import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message

from middlewares.HappyMonthMiddleware import UserInternalIdMiddleware, HappyMonthMiddleware

import tokenfile as tf

TOKEN = tf.TOKEN

bot_unit = Bot(token=TOKEN)

router = Router()


@router.message(Command("happymonth"))
async def cmd_happymonth(
        message: Message,
        internal_id: int,
        is_happy_month: bool
):
    phrases = [f"Ваш ID в нашем сервисе: {internal_id}"]
    if is_happy_month:
        phrases.append("Сейчас ваш счастливый месяц!")
    else:
        phrases.append("В этом месяце будьте осторожнее...")
    await message.answer(". ".join(phrases))


async def main(bot: Bot):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher()
    dp.include_routers(router)
    dp.update.outer_middleware(UserInternalIdMiddleware())
    router.message.middleware(HappyMonthMiddleware())

    # пропустить необработанные апдейты:
    # await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main(bot_unit))



