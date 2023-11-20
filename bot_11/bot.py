import asyncio
import logging

from aiogram import Bot, Dispatcher
from handlers import in_pm, bot_in_group, admin_changes_in_group, events_in_group
from middlewares.weekend import WeekendCallbackMiddleware
from middlewares.long_operation import ChatActionMiddleware

import tokenfile as tf

TOKEN = tf.TOKEN
OWNER_CHAT_ID = tf.OWNER_CHAT_ID
OWNER_CHANNEL_ID = tf.OWNER_CHANNEL_ID
OWNER_GROUP_NAME = tf.OWNER_GROUP_NAME

bot_unit = Bot(token=TOKEN)


async def set_up_routers(dp):
    dp.include_routers(
        bot_in_group.router,
        events_in_group.router,
        admin_changes_in_group.router,
        in_pm.router
    )
    dp.message.outer_middleware(ChatActionMiddleware())
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

    admin_ids = {}
    try:
        # Подгрузка списка админов
        admins = await bot.get_chat_administrators(chat_id=OWNER_GROUP_NAME)
        admin_ids = {admin.user.id for admin in admins}
        admins_list = [admin.user.first_name for admin in admins]
        print(f'Администраторы чата {OWNER_GROUP_NAME}: {admins_list}')
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    # await dp.start_polling(bot, allowed_updates=["message", "inline_query", "chat_member"])
    await dp.start_polling(bot, admins=admin_ids)


if __name__ == "__main__":
    asyncio.run(main(bot_unit))



