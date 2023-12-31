from datetime import datetime
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


def _is_weekend() -> bool:
    # 5 - суббота, 6 - воскресенье
    return datetime.utcnow().weekday() in (5, 6)


# Это будет inner-мидлварь на сообщения - будет навешан только в хендлере checkin.py
class WeekendMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Если сегодня не суббота и не воскресенье,
        # то продолжаем обработку.
        print('Работает WeekendMessageMiddleware(), проверяем выходные дни')
        if not _is_weekend():
            return await handler(event, data)
        # В противном случае просто вернётся None
        # и обработка прекратится
        # либо можно добавить сообщение:
        else:
            await event.answer(text='Бот не работает')


# Это будет outer-мидлварь на любые колбэки - он будет навешан на диспетчер в bot.py
class WeekendCallbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        # Если сегодня не суббота и не воскресенье,
        # то продолжаем обработку.
        print('РРаботает WeekendCallbackMiddleware(), проверяем выходные дни')
        if not _is_weekend():
            return await handler(event, data)
        # В противном случае отвечаем на колбэк самостоятельно
        # и прекращаем дальнейшую обработку
        await event.answer(
            "Бот по выходным не работает!",
            show_alert=True
        )
        return
