from random import randint
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.dispatcher.flags import get_flag


class MiddlewareAlfa(BaseMiddleware):
    def __init__(self, middleware_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = middleware_name

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        print(f'{self.name:20} {"start":>}: {data.get("first_random")} - {data.get("random")}')

        # Принимаем имя целевого хэндлера, если такого нет - считаем на данном этапе, что мидлварь is outer
        handler_name = get_flag(data, "handler_name")
        if handler_name is None:
            message_text = 'Это outer handler'
        else:
            message_text = f'Целевой хэндлер: {handler_name}'
        await event.answer(text=f'{self.name} - start. {message_text}')

        # Определяем значение random и first_random:
        data["random"] = randint(1, 100)
        if data.get("first_random") is None:
            data["first_random"] = data["random"]
        await event.answer(text=f'Выпало число {data["random"]} ({data["first_random"]})')

        print(f'{self.name:20} {"end":>5}: {data.get("first_random")} - {data.get("random")}')

        if data["random"] > 5:
            # Передаем полученный в мидлвари результат далее в хендлер (будет выведен на экран)
            result = await handler(event, data)
            await event.answer(text=f'{self.name} - end\nВы проходите дальше')
            return result
        else:
            await event.answer(text=f'{self.name} - end\nВы не прошли')


