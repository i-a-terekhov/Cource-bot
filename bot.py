import asyncio
import logging
from asyncio import sleep
from pprint import pprint

from aiogram.types import ChatMember, User
from aiogram import Bot, Dispatcher, exceptions
from handlers import checkin, group_games, usernames, questions, different_types, in_pm, bot_in_group
from middlewares.weekend import WeekendCallbackMiddleware
from middlewares.long_operation import ChatActionMiddleware

import tokenfile

TOKEN = tokenfile.TOKEN
OWNER_CHAT_ID = tokenfile.OWNER_CHAT_ID
OWNER_CHANNEL_ID = tokenfile.OWNER_CHANNEL_ID
OWNER_GROUP_ID = tokenfile.OWNER_GROUP_ID

bot_unit = Bot(token=TOKEN)


async def get_chat_id(bot: Bot, chat_id: int) -> bool:
    try:
        chat_member = await bot.get_chat_member(chat_id, user_id=bot.id)
        return chat_member.status in [ChatMember.ADMINISTRATOR, ChatMember.CREATOR]
    except exceptions.TelegramNotFound:
        return False


async def main(bot: Bot):
    try:
        print('начало')
        if await get_chat_id(bot, OWNER_GROUP_ID):
            print(f"Бот успешно получил информацию о чате {OWNER_GROUP_ID}")
            admins = await bot.get_chat_administrators(chat_id=OWNER_GROUP_ID)
            print("Бот имеет доступ к методу.")
            admin_ids = {admin.user.id for admin in admins}
            await dp.start_polling(bot, admins=admin_ids)
        else:
            print(f"Чат {OWNER_GROUP_ID} не найден или бот не имеет доступа.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Запуск бота
# async def main(bot: Bot):
#     # logging.basicConfig(
#     #     level=logging.INFO,
#     #     format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
#     # )
#
#     dp = Dispatcher()
#     # Порядок регистрации роутеров критичен. Апдейт, пойманный во втором роутере - не попадет в обработку к третьему:
#     dp.include_routers(
#         bot_in_group.router,
#         in_pm.router,
#         checkin.router,
#         group_games.router,
#         usernames.router,
#         questions.router,
#         different_types.router
#     )
#     dp.message.outer_middleware(ChatActionMiddleware())
#     dp.callback_query.outer_middleware(WeekendCallbackMiddleware())
#
#     # пропустить необработанные апдейты:
#     await bot.delete_webhook(drop_pending_updates=True)
#
#     await bot.send_message(chat_id=OWNER_CHAT_ID, text='Привет!')
#
#     try:
#         print(OWNER_GROUP_ID)
#         # chat = await bot.get_chat(chat_id=str(OWNER_GROUP_ID))
#         chat = await bot.send_chat_action(chat_id=OWNER_GROUP_ID, action="typing")
#         print(chat)
#
#         admins = await bot.get_chat_administrators(chat_id=OWNER_GROUP_ID)
#         print("Бот имеет доступ к методу.")
#         admin_ids = {admin.user.id for admin in admins}
#         await dp.start_polling(bot, admins=admin_ids)
#     except exceptions.TelegramAPIError as e:
#         pprint(e)
#         print(f"Произошла ошибка при запросе к Telegram API: {e}")
#     except Exception as e:
#         print(f"Произошла неожиданная ошибка: {e}")
#
#     # await dp.start_polling(bot, admins=admin_ids, allowed_updates=["message", "inline_query", "chat_member"])
#     # await dp.start_polling(bot)
#
#     await bot_unit.session.close()


if __name__ == "__main__":
    asyncio.run(main(bot_unit))
