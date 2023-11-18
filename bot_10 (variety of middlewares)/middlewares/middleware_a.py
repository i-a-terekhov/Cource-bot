from random import randint
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.dispatcher.flags import get_flag


class MiddlewareNoA(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        name = get_flag(data, "name")

        await event.answer(text=f'Middleware A - start. Подходящий хэндлер: {name}')
        random = randint(1, 100)

        await event.answer(text=f'Выпало число {random}')
        if random > 20:
            data["random"] = random
            result = await handler(event, data)
            await event.answer(text=f'Middleware A - end\nВы проходите дальше')
            return result
        else:
            await event.answer(text=f'Middleware A - end\nВы не прошли')


