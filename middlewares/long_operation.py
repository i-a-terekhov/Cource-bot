from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Message

from aiogram.dispatcher.flags import get_flag
from aiogram.utils.chat_action import ChatActionSender


class ChatActionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        long_operation_type = get_flag(data, "long_operation")

        # Если такого флага на хэндлере нет
        if not long_operation_type:
            print('не найдено длительной операции')
            return await handler(event, data)

        # Если флаг есть
        #TODO разобраться, почему не отправляется статус (даже не печатается принт), в аргументе не хватает bot?
        async with ChatActionSender(action=long_operation_type, chat_id=event.chat.id):
            print('идет длительная операция')
            return await handler(event, data)
