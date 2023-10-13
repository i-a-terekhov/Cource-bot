import asyncio
import logging
import sys
from os import getenv  # для запуска на https://replit.com

from aiogram.client import bot

import tokenfile  # для оффлайна

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
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
    'Не только парфюм'
]


@dp.message(CommandStart())
async def command_start_handler(message: Message, reply_ms=False, reply_cb=False) -> None:
    if reply_ms:
        await message.reply(f"Hello, {hbold(message.from_user.full_name)}!")
    else:
        await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")

    if reply_cb:
        builder, another_builder = ReplyKeyboardBuilder(), ReplyKeyboardBuilder()
    else:
        builder, another_builder = InlineKeyboardBuilder(), InlineKeyboardBuilder()

    for option in main_menu:
        builder.button(text=option, callback_data=f"set:{option}")  # TODO далее - написать хэндлер калбеков
    builder.adjust(1, 2, 2, 1)

    for index in range(11, 13):
        option = f"Еще что-то {index}"
        another_builder.button(text=option, callback_data=f"set:{option}")
    another_builder.button(text='Кушоц', callback_data='Кушоц')
    another_builder.adjust(3)
    builder.attach(another_builder)

    await message.answer(
        "Я - арома-бот, помогу Вам с подбором аромата! Вжуух!",
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )


@dp.callback_query(F.data.startswith('set:'))
async def set_button_handler(callback_query: types.CallbackQuery) -> None:
    user_react = callback_query.data.split(':')[1]
    await callback_query.message.answer(text=f"Вы выбрали пункт '{user_react}'! Сейчас я всё расскажу! ;)")


#TODO заменить обычную клавиатуру на инлайн:
@dp.callback_query(F.data == 'Кушоц')
async def pure(callback_query: types.CallbackQuery) -> None:
    kb = [
        [
            types.KeyboardButton(text="С пюрешкой"),
            types.KeyboardButton(text="Без пюрешки")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ подачи"
    )
    await callback_query.message.answer(text="Как подавать котлеты?", reply_markup=keyboard)


@dp.message(F.text.lower() == "с пюрешкой")
async def with_puree(message: types.Message):
    await message.answer("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())


@dp.message(F.text.lower() == "без пюрешки")
async def without_puree(message: types.Message):
    await message.answer("Так невкусно!", reply_markup=types.ReplyKeyboardRemove())


# Специальные обычные кнопки позволяют запросить гео и контакт юзера:
@dp.message(Command("special_buttons"))
async def cmd_special_buttons(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Запросить геолокацию", request_location=True),
        types.KeyboardButton(text="Запросить контакт", request_contact=True),
    )

    await message.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True),
    )


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
