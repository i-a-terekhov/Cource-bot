from aiogram import Router
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message
from aiogram.filters import Command

from filters.chat_type import ChatTypeFilter

# фильтр можно повесить как на весь роутер, так и на отдельные хэндлеры:
router = Router()

# Фильтр на тип чата можно сделать чуть иначе.
# Несмотря на то, что типов чатов у нас четыре (ЛС, группа, супергруппа, канал), апдейт типа message не может
# прилетать из каналов, т.к. у них свой апдейт channel_post.
# А когда мы фильтруем группы, обычно всё равно, обычная группа или супергруппа, лишь бы не личка.
#
# Таким образом, сам фильтр можно свести к условному ChatTypeFilter(is_group=True/False) и просто проверять,
# ЛС или не ЛС.
router.message.filter(
    ChatTypeFilter(chat_type=['group', 'supergroup', 'private'])
)


@router.message(Command(commands=['dice']))
async def cmd_dice_in_group(message: Message):
    await message.answer_dice(emoji=DiceEmoji.DICE)


@router.message(Command(commands=['basketball']))
async def cmd_basketball_in_group(message: Message):
    await message.answer_dice(emoji=DiceEmoji.BASKETBALL)