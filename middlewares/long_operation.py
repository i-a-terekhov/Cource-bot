from pprint import pprint

from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Message

from aiogram.dispatcher.flags import get_flag
from aiogram.utils.chat_action import ChatActionSender

dict_operations = {}


class ChatActionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        print(f'работает мидлварь long_operation')
        for key, value in data.items():
            if dict_operations.get(key):
                if dict_operations[key] == value:
                    print(f'{key:20} не изменился')
                else:
                    print(f'{key:20} -->X {dict_operations[key].__dict__}\n{key:20} ~~~> {value.__dict__}')
                    dict_operations[key] = value
            else:
                dict_operations[key] = value
                print(f'{key:20} ---> {value}')

        long_operation_type = get_flag(data, "long_operation")
        # pprint(data)
        print(f'\tлонг оператион тайп {long_operation_type}')

        # Если такого флага на хэндлере нет
        if not long_operation_type:
            print('\t\tне найдено длительной операции')
            return await handler(event, data)

        # Если флаг есть
        else:
            async with ChatActionSender(action=long_operation_type, chat_id=event.chat.id, bot=data['bot']):
                print('\t\tидет длительная операция')
                return await handler(event, data)
