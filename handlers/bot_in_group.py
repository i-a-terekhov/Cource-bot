from asyncio import sleep

from aiogram import F, Router
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, JOIN_TRANSITION, LEAVE_TRANSITION
from aiogram.types import ChatMemberUpdated

from bot import bot_unit, OWNER_CHAT_ID

router = Router()
router.chat_member.filter(F.chat.type.in_({'group', 'supergroup', 'channel'}))

chats_variants = {
    "group": "группу",
    "supergroup": "супергруппу",
    "channel": "канал",
}

chats_variants_exit = {
    "group": "группы",
    "supergroup": "супергруппы",
    "channel": "канала",
}


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def bot_added_as_admin(event: ChatMemberUpdated):
    mess_text = f'Бот добавлен в {chats_variants[event.chat.type]} {event.chat.title}, ID {event.chat.id}'
    print(mess_text)
    await bot_unit.send_message(chat_id=OWNER_CHAT_ID, text=mess_text)

    await sleep(3)
    await event.answer(
        text=f"Привет! Спасибо, что добавили меня в {chats_variants[event.chat.type]} '{event.chat.title}'!"
    )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION))
async def bot_kicked(event: ChatMemberUpdated):
    mess_text = f'Бот удален из {chats_variants_exit[event.chat.type]} {event.chat.title}, ID {event.chat.id}'
    print(mess_text)
    await bot_unit.send_message(chat_id=OWNER_CHAT_ID, text=mess_text)
