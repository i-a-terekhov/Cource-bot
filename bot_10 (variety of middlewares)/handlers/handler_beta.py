from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from middlewares.middleware_alfa import MiddlewareAlfa


router = Router()
# Несмотря на намеренно нелогичный порядок определения мидлварей ниже, вначале всегда выполняются outer:
router.message.middleware(MiddlewareAlfa(middleware_name="Middleware_D(beta)"))
router.message.outer_middleware(MiddlewareAlfa(middleware_name="Middleware_B(beta)"))


# Можно передать в мидлварь какие-то свои значения (например: handler_name).
# Передавать данные из мидлварей можно через словарь data, который в мидлварях
# будет получать значения в виде пар ключ-значение,
# а в хендлере эти значения будут принимать приниматься через ключи в параметрах:

@router.message(Command("start"), flags={"handler_name": "Handler_beta"})
async def cmd_checkin(message: Message, random: int, first_random: int):
    print(f'{__name__:26}: {first_random} - {random}')
    await message.answer(text=f'Handler B - working')
