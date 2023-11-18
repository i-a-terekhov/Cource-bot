from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from middlewares.middleware_a import MiddlewareNoA


router = Router()
router.message.middleware(MiddlewareNoA())


# TODO объяснить двойное срабатывание мидлваря_альфа: с флагом и без
# можно передать в хэндлер какие-то свои параметры (например: name):
@router.message(Command("start"), flags={"name": "Handler_alfa"})
async def cmd_checkin(message: Message, random: int):
    print(random)
    await message.answer(text=f'Handler A - working')
