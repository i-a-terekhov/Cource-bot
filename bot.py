import asyncio
import logging
from asyncio import sleep
from pprint import pprint

from aiogram.types import ChatMember, User
from aiogram import Bot, Dispatcher, exceptions
from handlers import checkin, group_games, usernames, questions, different_types, in_pm, bot_in_group
from middlewares.weekend import WeekendCallbackMiddleware
from middlewares.long_operation import ChatActionMiddleware

import tokenfile as tf

TOKEN = tf.TOKEN
OWNER_CHAT_ID = tf.OWNER_CHAT_ID
OWNER_CHANNEL_ID = tf.OWNER_CHANNEL_ID
OWNER_GROUP_NAME = tf.OWNER_GROUP_NAME

bot_unit = Bot(token=TOKEN)


async def main(bot: Bot):
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    # )

    dp = Dispatcher()
    # Порядок регистрации роутеров критичен. Апдейт, пойманный во втором роутере - не попадет в обработку к третьему:
    dp.include_routers(
        bot_in_group.router,
        in_pm.router,
        checkin.router,
        group_games.router,
        usernames.router,
        questions.router,
        different_types.router
    )
    dp.message.outer_middleware(ChatActionMiddleware())
    dp.callback_query.outer_middleware(WeekendCallbackMiddleware())

    # пропустить необработанные апдейты:
    # await bot.delete_webhook(drop_pending_updates=True)

    try:
        if await bot.get_chat(OWNER_GROUP_NAME):
            print(f"Бот успешно нашел чат {OWNER_GROUP_NAME}")
            if await bot.get_chat_administrators(chat_id=OWNER_GROUP_NAME):
                admins = await bot.get_chat_administrators(chat_id=OWNER_GROUP_NAME)
                admins = {admin.user.first_name for admin in admins}
                print(f'Администраторы чата {OWNER_GROUP_NAME}: {admins}')
        else:
            print(f"Чат {OWNER_GROUP_NAME} не найден или бот не имеет доступа.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    # await dp.start_polling(bot, admins=admin_ids, allowed_updates=["message", "inline_query", "chat_member"])
    await dp.start_polling(bot, allowed_updates=["message", "inline_query", "chat_member"])
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main(bot_unit))
