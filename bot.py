import asyncio
from aiogram import Bot, Dispatcher
from handlers import checkin, group_games, usernames, questions, different_types, in_pm
from middlewares.weekend import WeekendCallbackMiddleware
from middlewares.long_operation import ChatActionMiddleware

import tokenfile

TOKEN = tokenfile.token


# Запуск бота
async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Порядок регистрации роутеров критичен. Апдейт, пояманный во втором роутере - не попадет в обработку к третьему:
    dp.include_routers(
        in_pm.router,
        checkin.router,
        group_games.router,
        usernames.router,
        questions.router,
        different_types.router
    )
    dp.message.outer_middleware(ChatActionMiddleware())
    dp.callback_query.outer_middleware(WeekendCallbackMiddleware())

    # Альтернативный вариант регистрации роутеров по одному на строку
    # dp.include_router(questions.router)
    # dp.include_router(different_types.router)

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
