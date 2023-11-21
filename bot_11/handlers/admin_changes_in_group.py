from aiogram import F, Router
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter,\
    KICKED, LEFT, RESTRICTED, MEMBER, ADMINISTRATOR, CREATOR
from aiogram.types import ChatMemberUpdated

from tokenfile import OWNER_CHANNEL_ID

router = Router()
router.chat_member.filter(F.chat.id == OWNER_CHANNEL_ID)

# Событие chat_member.
# Содержит все изменения состояния пользователей в группах и каналах, где бот состоит в качестве
# администратора: приход/уход юзеров в группы, подписки/отписки в каналах, изменение прав и статусов пользователей,
# назначение/снятие админов и многое другое.


@router.chat_member(ChatMemberUpdatedFilter(
        member_status_changed=(KICKED | LEFT | RESTRICTED | MEMBER) >> (ADMINISTRATOR | CREATOR)
    ))
async def admin_promoted(event: ChatMemberUpdated, admins: set[int]):
    admins.add(event.new_chat_member.user.id)
    await event.answer(
        f"{event.new_chat_member.user.first_name} "
        f"был(а) повышен(а) до Администратора!"
    )


@router.chat_member(ChatMemberUpdatedFilter(
        member_status_changed=(KICKED | LEFT | RESTRICTED | MEMBER) << (ADMINISTRATOR | CREATOR)
    ))
async def admin_demoted(event: ChatMemberUpdated, admins: set[int]):
    admins.discard(event.new_chat_member.user.id)
    await event.answer(
        f"{event.new_chat_member.user.first_name} "
        f"был(а) понижен(а) до обычного юзера!"
    )