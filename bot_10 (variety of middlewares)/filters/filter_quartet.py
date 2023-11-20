from aiogram.filters import BaseFilter
from aiogram.types import Message


class FiftyPercentFilter(BaseFilter):
    async def __call__(self, message: Message, random: int, first_random: int):
        print(f'{"Filter":26}: {first_random} - {random}', end='  : ')
        if random >= 30:
            print('True')
            await message.answer(text=f'Фильтр преодолен!')
            return True
        print('False')
        await message.answer(text=f'Фильтр не пропустил апдейт')
        return False
