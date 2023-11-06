from asyncio import sleep
from pprint import pprint

from aiogram import F, Router, Bot
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_NOT_MEMBER, KICKED, MEMBER, ADMINISTRATOR, IS_MEMBER
from aiogram.types import ChatMemberUpdated, Message

from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, JOIN_TRANSITION

from bot import bot_unit, OWNER_CHAT_ID

router = Router()
router.chat_member.filter(F.chat.type.in_({'group', 'supergroup', 'channel'}))

chats_variants = {
    "group": "группу",
    "supergroup": "супергруппу",
    "channel": "канал",
}


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> ADMINISTRATOR))
async def bot_added_as_admin(event: ChatMemberUpdated):
    print(f'Бот добавлен как админ в чат {event.chat.title}')
    # print(event.chat.type)
    # print(event.chat.title)
    # print(event.chat.id)
    # print(event.chat.permissions)
    await sleep(3)
    await event.answer(
        text=f"Привет! Спасибо, что добавили "
             f"меня в {chats_variants[event.chat.type]} '{event.chat.title}' как администратора. "
             f"ID чата: {event.chat.id}"
    )
    await bot_unit.send_message(chat_id=OWNER_CHAT_ID, text='Бота добавили в группу')


# Не получилось проверить возможность написания комментов ботом:
# Не получилось проверить реакцию на добавление бота как простого участника, т.к. в телеге не найдено такой возможности
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> MEMBER))
async def bot_added_as_member(event: ChatMemberUpdated):
    await sleep(3)
    await event.answer(
        text=f"Привет! Спасибо, что добавили меня в "
             f'{chats_variants[event.chat.type]} "{event.chat.title}" '
             f"как обычного участника. ID чата: {event.chat.id}"
    )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=ADMINISTRATOR >> IS_NOT_MEMBER))
async def bot_kicked(event: ChatMemberUpdated):
    print(f'Бота удалили из группы {event.chat.title}')
    mess_text = f'Бота удалили из группы {event.chat.title}, ID - {event.chat.id}'
    await bot_unit.send_message(chat_id=OWNER_CHAT_ID, text=mess_text)
