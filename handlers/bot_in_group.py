from aiogram import F, Router
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_NOT_MEMBER, KICKED, MEMBER, ADMINISTRATOR, IS_MEMBER
from aiogram.types import ChatMemberUpdated

from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, JOIN_TRANSITION

router = Router()
router.chat_member.filter(F.chat.type.in_({'group', 'supergroup'}))


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def wow(event: ChatMemberUpdated):
    print('получилось?')

chats_variants = {
    "group": "группу",
    "supergroup": "супергруппу"
}


#TODO эта функция кидает исключения:
@router.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def bot_added_as_member(event: ChatMemberUpdated):
    print('Сработал фильтр на мембера')
    await event.answer(
        text=f"Привет! Спасибо, что добавили меня в "
             # f'{chats_variants[event.chat.type]} "{event.chat.title}" '
             # f"как администратора. ID чата: {event.chat.id}"
    )


# @router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> MEMBER))
# async def bot_added_as_member(event: ChatMemberUpdated):
#     # Вариант посложнее: бота добавили как обычного участника.
#     # Но может отсутствовать право написания сообщений, поэтому заранее проверим.
#     chat_info = await bot.get_chat(event.chat.id)
#     if chat_info.permissions.can_send_messages:
#         await event.answer(
#             text=f"Привет! Спасибо, что добавили меня в "
#                  f'{chats_variants[event.chat.type]} "{event.chat.title}" '
#                  f"как обычного участника. ID чата: {event.chat.id}"
#         )
#     else:
#         print("Как-нибудь логируем эту ситуацию")