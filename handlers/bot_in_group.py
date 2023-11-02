from aiogram import F, Bot, Router
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER, ADMINISTRATOR
from aiogram.types import ChatMemberUpdated

router = Router()
router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))

chats_variants = {
    "group": "группу",
    "supergroup": "супергруппу"
}

#TODO тесты и изменения кода не помогли, бот не выводит эти сообщения. Как такогого, результата на сегодня нет.

@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> ADMINISTRATOR))
async def bot_added_as_admin(event: ChatMemberUpdated):
    # Самый простой случай: бот добавлен как админ.
    # Легко можем отправить сообщение
    print('сработка 1')
    await event.answer(
        text=f"Привет! Спасибо, что добавили меня в "
             f'{chats_variants[event.chat.type]} "{event.chat.title}" '
             f"как администратора. ID чата: {event.chat.id}"
    )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> MEMBER))
async def bot_added_as_member(event: ChatMemberUpdated, bot: Bot):
    # Вариант посложнее: бота добавили как обычного участника.
    # Но может отсутствовать право написания сообщений, поэтому заранее проверим.
    chat_info = await bot.get_chat(event.chat.id)
    if chat_info.permissions.can_send_messages:
        await event.answer(
            text=f"Привет! Спасибо, что добавили меня в "
                 f'{chats_variants[event.chat.type]} "{event.chat.title}" '
                 f"как обычного участника. ID чата: {event.chat.id}"
        )
    else:
        print("Как-нибудь логируем эту ситуацию")