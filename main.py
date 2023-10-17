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
from aiogram.utils.chat_action import ChatActionSender

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
    # await delete_message(message)  # удаляет сообщение пользователя (т.е. '\start', в данном случае)
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
    another_builder.button(text='Рандом', callback_data='random')
    another_builder.button(text='Очистить чат', callback_data='clear')
    another_builder.adjust(3)
    builder.attach(another_builder)
    await message.answer(
        "Я - арома-бот, помогу с подбором аромата! Вжуух!",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


@dp.callback_query(F.data.startswith('set:'))
async def set_button_handler(callback: types.CallbackQuery) -> None:
    await callback.answer()  # Данный callback.answer() нужен только для того, чтобы на андройде
    # не проигрывалась анимация ожидания у нажатой кнопки (белый волнообразный градиент). У яблока такого нет
    user_react = callback.data.split(':')[1]
    await callback.message.answer(
        reply_markup=ReplyKeyboardRemove(),
        text=f"Вы выбрали пункт '{user_react}'! Сейчас я всё расскажу! ;)",
    )


@dp.callback_query(F.data == 'кушоц')
async def pure(callback: types.CallbackQuery) -> None:
    await callback.answer()
    keyboard_inline = InlineKeyboardBuilder()
    keyboard_inline.button(text='С пюрешкой', callback_data='с пюрешкой')
    keyboard_inline.button(text='Без пюрешки', callback_data='без пюрешки')
    keyboard_inline.adjust(2)
    await callback.message.answer(
        text="Как подавать котлеты?",
        reply_markup=keyboard_inline.as_markup(resize_keyboard=True)
    )


@dp.callback_query(F.data == 'с пюрешкой')
async def with_puree(callback: types.CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer("Отличный выбор!")


@dp.callback_query(F.data == 'без пюрешки')
async def without_puree(callback: types.CallbackQuery) -> None:
    # await callback.answer()
    await callback.message.answer("Так невкусно!")


# В процессе использования выяснилось, что при нажатии на кнопки с request_location и request_contact
# не срабатывает one_time_keyboard. В качестве костыля предлагается во всех хендлерах прописывать
# аргумент для answer => reply_markup=ReplyKeyboardRemove() либо добавлять кнопку-пустышку
# Специальные обычные кнопки позволяют запросить гео и контакт юзера:
@dp.callback_query(F.data == 'спец')
async def cmd_special_buttons(callback: types.CallbackQuery) -> None:
    await callback.answer()
    builder = ReplyKeyboardBuilder()
    builder.button(text="Отправить геолокацию", request_location=True),
    builder.button(text="Отправить контакт", request_contact=True),
    builder.button(text='Убрать клавиатуру')
    await callback.message.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup(
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


@dp.message(F.text == 'Убрать клавиатуру')
async def del_message(message: Message) -> None:
    await message.answer(text='Специальная клавиатура убрана', reply_markup=ReplyKeyboardRemove())


@dp.callback_query(F.data == 'random')
async def callrandfunc(callback: types.CallbackQuery):
    await callback.answer()
    await cmd_random(callback.message)


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
    # await callback.answer()
    await callback.message.answer(str(randint(1, 10)))
    await callback.answer(
        text="Спасибо, что воспользовались генератором случайных целых чисел от одного до десяти!\n"
             "В следующей версии генератор сможет выдать целые числа от одного до ДВАДЦАТИ!",
        show_alert=True  # Если Fasle - отображается вверху экрана, если True - выводится всплывающее сообщение
    )
    #TODO проверить в остальных калбек-хендлерах наличие второго callback.answer() потому что:
    await callback.answer(text='второй текст не выводится')  # вероятно, callback.answer() срабатывает только один раз
    print('Функция рандома отработала')



@dp.message(Command('clear'))
async def cmd_clear(message: types.Message, bot: Bot, del_forward: None) -> None:
    # выводит "печатает" во время работы функции:
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id, interval=3.0):
        deleted_message = []
        del_forward = False
        if not del_forward:
            deleted_message = ['функция сохранения удаляемых сообщений была отключена']
        print(f'Запрошено удаление сообщений в чате с id={message.chat.id}')

        for i in range(message.message_id, message.message_id - 50, -1):
            try:
                if del_forward:
                    # пересылка сообщений - это "костыль", позволяющий сохранить текст сообщений:
                    ex_message = await bot.forward_message(
                        chat_id=message.chat.id,
                        from_chat_id=message.chat.id,
                        message_id=i)
                    if ex_message:
                        deleted_message.append(ex_message.text)
                        await bot.delete_message(message.chat.id, ex_message.message_id)
                await bot.delete_message(message.chat.id, i)
            except:
                pass
        print('Удалены сообщения', deleted_message)
        # await message.answer('/start')


@dp.callback_query(F.data == "clear")
async def clear(callback: types.CallbackQuery):
    await callback.answer()
    await cmd_clear(callback.message, dp.bot, None)


# эхо-функция
@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        if types.ContentType.TEXT == message.content_type:
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
