import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from tokenfile import TOKEN
from handlers import common, save_text, save_images, \
    inline_mode, delete_data, inline_pagination_demo, \
    inline_chosen_result_demo


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Для демонстрационных целей используем "оперативную память" - она ненадежна и сбрасывается при перезапуске:
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(TOKEN)

    dp.include_routers(
        common.router,
        save_text.router, save_images.router, delete_data.router,
        inline_mode.router, inline_pagination_demo.router,
        inline_chosen_result_demo.router
    )

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
