from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from middlewares.middleware_alfa import MiddlewareAlfa


router = Router()
# Несмотря на намеренно нелогичный порядок определения мидлварей ниже, вначале всегда выполняются outer:
router.message.middleware(MiddlewareAlfa(middleware_name="Middleware_D(beta)"))
router.message.outer_middleware(MiddlewareAlfa(middleware_name="Middleware_B(beta)"))


# TODO объяснить двойное срабатывание мидлваря_альфа: с флагом и без
# можно передать в мидлварь какие-то свои параметры (например: handler_name):
@router.message(Command("start"), flags={"handler_name": "Handler_beta"})
async def cmd_checkin(message: Message, data: dict):
    print(data)
    await message.answer(text=f'Handler B - working')
