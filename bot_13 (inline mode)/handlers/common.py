from aiogram import Router, F
from aiogram.filters.command import Command, CommandStart
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, \
    InlineKeyboardMarkup, InlineKeyboardButton

from states import SaveCommon, DeleteCommon

router = Router()


#  Это фильтр команды, который указывает, что функция cmd_save должна вызываться только в том случае,
#  если сообщение является командой /start и при этом в команде есть аргумент add. Практическое применение сомнительное
#  Более удобная точка входа в cmd_save() реализована во втором декораторе
@router.message(CommandStart(magic=F.args == "add"))
@router.message(Command("save"), StateFilter(None))
async def cmd_save(message: Message, state: FSMContext):
    await message.answer(
        text="Давай что-нибудь сохраним. "
             "Пришли мне какую-нибудь ссылку или картинку. "
             "Если передумаешь — шли /cancel"
    )
    await state.set_state(SaveCommon.waiting_for_save_start)


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Если хочешь что-то сохранить, введи /save"
             "Если желаешь что-то удалить, введи /delete",
        reply_markup=ReplyKeyboardRemove()
    )


#  Функция cmd_delete() рисует две кнопки, в каждой из которых используется переход в нужный инлайн-режим.
#  Параметр switch_inline_query_current_chat отправляется как дополнительная информация при отправке сообщения
#  или ответа в инлайн-режиме. Этот параметр говорит клиенту Telegram, что пользователю следует использовать
#  текущий чат (из которого был вызван инлайн-режим) для отправки запроса вместо общего чата или личных сообщений.
#  Обработчик события типа inline_query - в модуле inline_mode.py
@router.message(Command("delete"), StateFilter(None))
async def cmd_delete(message: Message, state: FSMContext):
    kb = []
    kb.append([
        InlineKeyboardButton(
            text="Выбрать ссылку",
            switch_inline_query_current_chat="links"
        )
    ])
    kb.append([
        InlineKeyboardButton(
            text="Выбрать изображение",
            switch_inline_query_current_chat="images"
        )
    ])
    await state.set_state(DeleteCommon.waiting_for_delete_start)
    await message.answer(
        text="Выберите, что хотите удалить:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
    )


@router.message(Command(commands=["cancel"]))
async def cmd_save(message: Message, state: FSMContext):
    await message.answer("Действие отменено")
    await state.clear()
