import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from tokenfile import TOKEN
from handlers import inline_mode, save_images, save_text


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Если не указать storage, то по умолчанию всё равно будет MemoryStorage
    # Но явное лучше неявного =]
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(TOKEN)

    dp.include_routers(
        inline_mode.router,
        save_images.router,
        save_text.router
    )

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
