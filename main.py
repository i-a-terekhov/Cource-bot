import asyncio
import logging
import sys
from os import getenv  # для запуска на https://replit.com
from random import randint

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
from aiogram.exceptions import TelegramBadRequest


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


# При удалении стартового сообщения от пользователя, в чате остается висеть плашка "Нажмите здесь, чтобы начать общение"
async def delete_message(message: types.Message):
    await asyncio.sleep(1)  # Ждем 1 секунду
    await message.delete()  # Удаляем сообщение


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await delete_message(message)  # удаляет сообщение пользователя (т.е. '\start', в данном случае)
    await message.answer(
        f"Привет, {hbold(message.from_user.full_name)}!",
        reply_markup=ReplyKeyboardRemove()
    )
    print(f'INFO: боту написал пользователь: {message.from_user.full_name}')

    builder, another_builder = InlineKeyboardBuilder(), InlineKeyboardBuilder()
    for option in main_menu:
        builder.button(text=option, callback_data=f"set:{option}")
    builder.adjust(1, 2, 2, 1)

    another_builder = InlineKeyboardBuilder()
    another_builder.button(text='Кушоц', callback_data='кушоц')
    another_builder.button(text='Спец', callback_data='спец')
    another_builder.button(text='Instagram', url="https://instagram.com/cloud.parfume?igshid=MzRlODBiNWFlZA==")
    another_builder.button(text='Очистить чат', callback_data='clear')
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


# В процессе использования выяснилось, что при нажатии на кнопки с request_location и request_contact
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


@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Нажми меня",
        callback_data="random_value")
    )
    await message.answer(
        "Нажмите на кнопку, чтобы бот отправил число от 1 до 10",
        reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data == "random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))

    # await callback.message.answer(callback.from_user.full_name)
    # await callback.message.answer(callback.from_user.language_code)
    # dict_of_model_config = callback.from_user.model_config.items()
    # string_items = ''
    # for name, val in dict_of_model_config:
    #     string_items += name + ': ' + str(val) + '\n'
    # await callback.message.answer(string_items)

    # Если вызывать callback.message.answer на андройде, кнопка "Нажми меня" будет 30 сек. анимироваться как ожидающая
    # ответа. Но если добавить callback.answer(), анимация не наблюдается:
    await callback.answer(
        text="Спасибо, что воспользовались генератором случайных целых чисел от одного до десяти!\n"
             "В следующей версии генератор сможет выдать целые числа от одного до ДВАДЦАТИ!",
        show_alert=False  # Если Fasle - отображается вверху экрана, если True - выводится всплывающее сообщение
    )


@dp.message(Command('clear'))
async def cmd_clear(message: types.Message, bot: Bot) -> None:
    print(f'Запрошено удаление сообщений в чате с id={message.chat.id}')
    #TODO в данной конфигурации цикл продолжается последние 50 номеров для сообщений, это могут быть как "сообщения",
    # так и "удаленные сообщения". Сообщения, написанные после кнопки "Очистить чат" - остаются.
    for i in range(message.message_id, message.message_id - 50, -1):
        try:
            await bot.delete_message(message.chat.id, i)
        except Exception as ex:
            pass # print(ex)
    await message.answer('/start')


@dp.callback_query(F.data == "clear")
async def clear(callback: types.CallbackQuery):
    await cmd_clear(callback.message, dp.bot)


# эхо-функция
# TODO сделать эхо только текста
@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Хорошая попытка! Попробуйте еще раз!")


@dp.message()
async def ignor_message(message: Message) -> None:
    pass


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp.bot = bot
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
