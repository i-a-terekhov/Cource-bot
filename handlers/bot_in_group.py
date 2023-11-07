from asyncio import sleep

from aiogram import F, Router
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter,\
    LEAVE_TRANSITION, IS_NOT_MEMBER, MEMBER, ADMINISTRATOR
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


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> MEMBER)
)
async def bot_added_as_member(event: ChatMemberUpdated):
    mess_text = f'Бот добавлен в {chats_variants[event.chat.type]} {event.chat.title}, ID {event.chat.id} как участник'
    print(mess_text)
    await bot_unit.send_message(chat_id=OWNER_CHAT_ID, text=mess_text)

    chat_info = await bot_unit.get_chat(event.chat.id)
    if chat_info.permissions.can_send_messages:
        await event.answer(
            text=f"Привет! Спасибо, что добавили меня в {chats_variants[event.chat.type]} '{event.chat.title}'!"
        )
    else:
        await bot_unit.send_message(chat_id=OWNER_CHAT_ID, text='Бот не может писать в чате')


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> ADMINISTRATOR))
async def bot_added_as_admin(event: ChatMemberUpdated):
    mess_text = f'Бот добавлен в {chats_variants[event.chat.type]} {event.chat.title}, ID {event.chat.id} как админ'
    print(mess_text)
    await bot_unit.send_message(chat_id=OWNER_CHAT_ID, text=mess_text)

    await sleep(3)
    await event.answer(
        text=f"Привет! Спасибо, что добавили меня в {chats_variants[event.chat.type]} '{event.chat.title}'!"
    )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER >> ADMINISTRATOR))
async def bot_added_as_admin(event: ChatMemberUpdated):
    mess_text = f'Бота назначили админом в {chats_variants[event.chat.type]} {event.chat.title}, ID {event.chat.id}'
    print(mess_text)
    await bot_unit.send_message(chat_id=OWNER_CHAT_ID, text=mess_text)

    await sleep(3)
    await event.answer(
        text=f"Я теперь админ!"
    )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=ADMINISTRATOR >> MEMBER))
async def bot_added_as_admin(event: ChatMemberUpdated):
    mess_text = f'С бота сняли админку в {event.chat.title}, ID {event.chat.id}'
    print(mess_text)
    await bot_unit.send_message(chat_id=OWNER_CHAT_ID, text=mess_text)

    await sleep(3)
    await event.answer(
        text=f"Я более не админ... Вы об этом пожалеете, кожаные ублюдки!"
    )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION))
async def bot_kicked(event: ChatMemberUpdated):
    mess_text = f'Бот удален из {chats_variants_exit[event.chat.type]} {event.chat.title}, ID {event.chat.id}'
    print(mess_text)
    await bot_unit.send_message(chat_id=OWNER_CHAT_ID, text=mess_text)
