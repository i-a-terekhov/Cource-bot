import asyncio
import logging
import sys
from os import getenv  # для запуска на https://replit.com

from aiogram.client import bot

import tokenfile  # для оффлайна

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import F

# TOKEN = getenv("toren")  # для запуска на https://replit.com
TOKEN = tokenfile.token  # для оффлайна

dp = Dispatcher()

main_menu = [
    'Ароматы',
    'О нас',
    'Где затестить',
    'Объемы',
    'Доставка',
    'Не только парфюм',
]


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!", reply_markup=ReplyKeyboardRemove())

    builder, another_builder = InlineKeyboardBuilder(), InlineKeyboardBuilder()
    for option in main_menu:
        builder.button(text=option, callback_data=f"set:{option}")
    builder.adjust(1, 2, 2, 1)

    another_builder = InlineKeyboardBuilder()
    another_builder.button(text='Кушоц', callback_data='кушоц')
    another_builder.button(text='Спец', callback_data='спец')
    another_builder.button(text='Instagram', url="https://instagram.com/cloud.parfume?igshid=MzRlODBiNWFlZA==")
    another_builder.adjust(3)
    builder.attach(another_builder)
    await message.answer(
        "Я - арома-бот, помогу с подбором аромата! Вжуух!",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


@dp.callback_query(F.data.startswith('set:'))
async def set_button_handler(callback_query: types.CallbackQuery) -> None:
    user_react = callback_query.data.split(':')[1]
    await callback_query.message.answer(
        reply_markup=ReplyKeyboardRemove(),
        text=f"Вы выбрали пункт '{user_react}'! Сейчас я всё расскажу! ;)",
    )


@dp.callback_query(F.data == 'кушоц')
async def pure(callback_query: types.CallbackQuery) -> None:
    keyboard_inline = InlineKeyboardBuilder()
    keyboard_inline.button(text='С пюрешкой', callback_data='с пюрешкой')
    keyboard_inline.button(text='Без пюрешки', callback_data='без пюрешки')
    keyboard_inline.adjust(2)
    await callback_query.message.answer(
        text="Как подавать котлеты?",
        reply_markup=keyboard_inline.as_markup(resize_keyboard=True)
    )


@dp.callback_query(F.data == 'с пюрешкой')
async def with_puree(callback_query: types.CallbackQuery) -> None:
    await callback_query.message.answer("Отличный выбор!")


@dp.callback_query(F.data == 'без пюрешки')
async def without_puree(callback_query: types.CallbackQuery) -> None:
    await callback_query.message.answer("Так невкусно!")


#TODO в процессе использования выяснилось, что при нажатии на кнопки с request_location и request_contact
# не срабатывает one_time_keyboard. В качестве костыля предлагается во всех хендлерах прописывать
# аргумент для answer => reply_markup=ReplyKeyboardRemove() либо добавлять кнопку-пустышку

# Специальные обычные кнопки позволяют запросить гео и контакт юзера:
@dp.callback_query(F.data == 'спец')
async def cmd_special_buttons(callback_query: types.CallbackQuery) -> None:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Отправить геолокацию", request_location=True),
    builder.button(text="Отправить контакт", request_contact=True),
    builder.button(text='Убрать клавиатуру')
    await callback_query.message.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup(
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


@dp.message(F.text == 'Убрать клавиатуру')
async def del_message(message: Message) -> None:
    await message.answer(text='Специальная клавиатура убрана', reply_markup=ReplyKeyboardRemove())

# эхо-функция
#TODO сделать эхо только текста
@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Хорошая попытка! Попробуйте еще раз!")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
