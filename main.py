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



# Добавление обычных кнопок (т.е. таких, которые транслируют в чат то, что на них написано)
@dp.message(Command("reply_builder"))
async def reply_builder(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 17):
        builder.add(types.KeyboardButton(text=str(i)+" действие такое-то"))
    builder.adjust(4)
    await message.answer(
        "Выберите число:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


# функция set_button_handler вызывается только при получении
# callback-запросов, у которых callback_data начинается с "set:":
@dp.callback_query(lambda c: c.data.startswith('set:'))  # TODO заменить лямбда-функцию на F-фильтр!
async def set_button_handler(callback_query: types.CallbackQuery) -> None:
    index = int(callback_query.data.split(':')[1])
    #TODO понять, как слать сообщение о нажатой кнопке непосредственно в чат, а не только как callback_query.answer():
    await callback_query.answer(chat_id=callback_query.from_user.id, text=f"Вы нажали на кнопку {index}")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")  # простое сообщение в чат
    await message.reply("Как твои дела?")  # сообщение "в ответ", с цитированием реплики пользователя

    builder = InlineKeyboardBuilder()
    for index in range(1, 11):
        builder.button(text=f"Кнопка {index}", callback_data=f"set:{index}")
    builder.adjust(3, 2, 3)

    another_builder = InlineKeyboardBuilder()
    for index in range(11, 21):
        another_builder.button(text=f"Кнопка {index}", callback_data=f"set:{index}")
    another_builder.adjust(1, 2, 3, 4)
    builder.attach(another_builder)  # присоседим another_builder к builder

    await message.answer("Some text here", reply_markup=builder.as_markup())


@dp.message(Command("pure"))
async def pure(message: types.Message):
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
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)


@dp.message(F.text.lower() == "с пюрешкой")
async def with_puree(message: types.Message):
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())


@dp.message(F.text.lower() == "без пюрешки")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно!", reply_markup=types.ReplyKeyboardRemove())


# ловим определенный ответ ("Ок"):
@dp.message()
async def how_are_you(message: Message) -> None:
    text = message.text  # Получение текста из сообщения
    user_id = message.from_user.id  # Получение ID пользователя
    if text == "Ок":
        await message.answer(f"Хорошо!")
    else:
        await message.answer(f"Похоже, ты, {user_id}, не ответил на мой вопрос.")


# эхо-функция:
@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
