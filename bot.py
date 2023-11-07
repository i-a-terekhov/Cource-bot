import asyncio
from aiogram import Bot, Dispatcher
from handlers import checkin, group_games, usernames, questions, different_types, in_pm, bot_in_group
from middlewares.weekend import WeekendCallbackMiddleware
from middlewares.long_operation import ChatActionMiddleware

import tokenfile

TOKEN = tokenfile.token
bot_unit = Bot(token=TOKEN)
OWNER_CHAT_ID = 5180054391


# Запуск бота
async def main(bot: Bot):
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
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main(bot=bot_unit))
