import asyncio
import logging
import time
from asyncio import sleep
from pprint import pprint
from threading import Thread

from aiogram.types import ChatMember, User
from aiogram import Bot, Dispatcher, exceptions
from handlers import checkin, group_games, usernames, questions, different_types, in_pm, bot_in_group, admin_changes_in_group, events_in_group
from middlewares.weekend import WeekendCallbackMiddleware
from middlewares.long_operation import ChatActionMiddleware

import tokenfile as tf

TOKEN = tf.TOKEN
TOKEN_TWO = tf.TOKEN_TWO
TOKEN_THREE = tf.TOKEN_THREE
OWNER_CHAT_ID = tf.OWNER_CHAT_ID
OWNER_CHANNEL_ID = tf.OWNER_CHANNEL_ID
OWNER_GROUP_NAME = tf.OWNER_GROUP_NAME

bot_unit = Bot(token=TOKEN)
bot_riot = Bot(token=TOKEN_TWO)
bot_citizen = Bot(token=TOKEN_THREE)


# TODO проблема заключается в том, что роутер можно подключить только к одному диспетчеру
async def set_up(dp):
    # Порядок регистрации роутеров критичен. Апдейт, пойманный во втором роутере - не попадет в обработку к третьему:
    dp.include_routers(
        bot_in_group.router,
        events_in_group.router,
        admin_changes_in_group.router,
        in_pm.router,
        checkin.router,
        group_games.router,
        usernames.router,
        questions.router,
        different_types.router
    )
    dp.message.outer_middleware(ChatActionMiddleware())
    dp.callback_query.outer_middleware(WeekendCallbackMiddleware())


async def main(bot: Bot):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher()
    await set_up(dp)

    # Подгрузка списка админов
    admins = await bot.get_chat_administrators(OWNER_GROUP_NAME)
    admin_ids = {admin.user.id for admin in admins}

    # пропустить необработанные апдейты:
    # await bot.delete_webhook(drop_pending_updates=True)

    try:
        admins = await bot.get_chat_administrators(chat_id=OWNER_GROUP_NAME)
        admins_list = [admin.user.first_name for admin in admins]
        print(f'Администраторы чата {OWNER_GROUP_NAME}: {admins_list}')
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    # await dp.start_polling(bot, allowed_updates=["message", "inline_query", "chat_member"])
    await dp.start_polling(bot, admins=admin_ids)


if __name__ == "__main__":
    # asyncio.run(main())

    bots_farm = [bot_unit, bot_riot, bot_citizen]

    loop = asyncio.get_event_loop()

    tasks = [main(token) for token, in zip(bots_farm)]

    loop.run_until_complete(asyncio.gather(*tasks))



