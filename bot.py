import asyncio
from aiogram import Bot, Dispatcher
from handlers import group_games, questions, different_types

import tokenfile

TOKEN = tokenfile.token


# Запуск бота
async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

# TODO разобраться, почему не подключается фильтр group_games.router:
    dp.include_routers(group_games.router, questions.router, different_types.router)

    # Альтернативный вариант регистрации роутеров по одному на строку
    # dp.include_router(questions.router)
    # dp.include_router(different_types.router)

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)  # TODO разобраться с webhook
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
