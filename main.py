import asyncio
import logging
import sys
from random import randint
from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardButton
from aiogram.utils.markdown import hbold
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder, InlineKeyboardMarkup
from aiogram import F
from aiogram.utils.chat_action import ChatActionSender
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram import exceptions
from contextlib import suppress

# from os import getenv  # для запуска на https://replit.com
import tokenfile  # для оффлайна

# TOKEN = getenv("toren")  # для запуска на https://replit.com
TOKEN = tokenfile.token  # для оффлайна

dp = Dispatcher()
# Такой мидлварь автоматически отвечает на любой калбек одной стандартной фразой, "перекрывая" прописанные в калбеках.
# Флаг pre отвечает за непереопределяемость callback.answer() внутри калбека
dp.callback_query.middleware(CallbackAnswerMiddleware(pre=False, text="Готово!", show_alert=True))

main_menu = [
    'Ароматы',
    'О нас',
    'Объемы',
    'Доставка',
]

user_data = {}


class NumbersCallbackFactory(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[int] = None


# При удалении стартового сообщения от пользователя, в чате остается висеть плашка "Нажмите здесь, чтобы начать общение"
async def delete_message(message: Message):
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
    builder.adjust(1, 2)

    another_builder = InlineKeyboardBuilder()
    another_builder.button(text='Кушоц', callback_data='кушоц')
    another_builder.button(text='Спец', callback_data='спец')
    another_builder.button(text='Instagram', url="https://instagram.com/cloud.parfume?igshid=MzRlODBiNWFlZA==")
    another_builder.button(text='Рандом', callback_data='random')
    another_builder.button(text='Нумератор', callback_data='cmd_numerate')
    another_builder.button(text='Очистить чат', callback_data='clear')
    another_builder.adjust(3)
    builder.attach(another_builder)
    await message.answer(
        "Я - арома-бот, помогу с подбором аромата! Вжуух!",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


@dp.callback_query(F.data.startswith('set:'))
async def set_button_handler(callback: CallbackQuery) -> None:
    await callback.answer()  # Данный callback.answer() нужен только для того, чтобы на андройде
    # не проигрывалась анимация ожидания у нажатой кнопки (белый волнообразный градиент). У яблока такого нет
    user_react = callback.data.split(':')[1]
    await callback.message.answer(
        reply_markup=ReplyKeyboardRemove(),
        text=f"Вы выбрали пункт '{user_react}'! Сейчас я всё расскажу! ;)",
    )


@dp.callback_query(F.data == 'кушоц')
async def pure(callback: CallbackQuery) -> None:
    # Для тестирования dp.callback_query.middleware() с аргументом pre:
    await callback.answer(text='Прекрасно!', show_alert=True)
    keyboard_inline = InlineKeyboardBuilder()
    keyboard_inline.button(text='С пюрешкой', callback_data='с пюрешкой')
    keyboard_inline.button(text='Без пюрешки', callback_data='без пюрешки')
    keyboard_inline.adjust(2)
    await callback.message.answer(
        text="Как подавать котлеты?",
        reply_markup=keyboard_inline.as_markup(resize_keyboard=True)
    )


@dp.callback_query(F.data == 'с пюрешкой')
async def with_puree(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer("Отличный выбор!")


@dp.callback_query(F.data == 'без пюрешки')
async def without_puree(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer("Так невкусно!")


# Специальные обычные кнопки позволяют запросить гео и контакт юзера.
# В процессе использования выяснилось, что при нажатии на кнопки с request_location и request_contact
# не срабатывает one_time_keyboard. В качестве костыля предлагается во всех хендлерах прописывать
# аргумент для callback.message.answer => reply_markup=ReplyKeyboardRemove() либо добавлять кнопку-пустышку
@dp.callback_query(F.data == 'спец')
async def cmd_special_buttons(callback: CallbackQuery) -> None:
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
async def callrandfunc(callback: CallbackQuery):
    await callback.answer()
    await cmd_random(callback.message)


@dp.message(Command("random"))
async def cmd_random(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Нажми меня",
        callback_data="random_value")
    )
    await message.answer(
        "Нажмите на кнопку, чтобы бот отправил число от 1 до 10",
        reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data == "random_value")
async def send_random_value(callback: CallbackQuery):
    # await callback.answer()
    compliments = [
        "Ты умница!",
        "Ты очень креативен!",
        "Ты всегда поднимаешь настроение!",
        "Ты такой добрый человек!",
        "Твой смех заразителен!",
        "Ты очень обаятелен!",
        "Ты всегда готов помочь!",
        "Ты такой талантливый!",
        "Ты светишь как солнце!",
        "Ты вдохновляешь меня!"
    ]
    rand_num = randint(1, len(compliments))
    await callback.message.answer(str(rand_num))
    await callback.answer(
        text=compliments[rand_num - 1],
        show_alert=True  # Если Fasle - отображается вверху экрана, если True - выводится всплывающее сообщение с "ОК"
    )
    await callback.answer(text='второй текст не выводится')  # вероятно, callback.answer() срабатывает только один раз


# Обычная клавиатура вывода "сообщения" и "обновленного сообщения" для функции numbers
# При множестве кнопок или сложно-составных калбеках - обрабатывать из становится затруднительно
def get_numbers_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="-2", callback_data="num_-2"),
            InlineKeyboardButton(text="-1", callback_data="num_-1"),
            InlineKeyboardButton(text="+1", callback_data="num_+1"),
            InlineKeyboardButton(text="+2", callback_data="num_+2")
        ],
        [InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# Альтернативная клавиатура, построенная с использованием фабрики калбеков NumbersCallbackFactory()
def get_numbers_keyboard_fab():
    builder = InlineKeyboardBuilder()
    builder.button(text="-2", callback_data=NumbersCallbackFactory(action="change", value=-2))
    builder.button(text="-1", callback_data=NumbersCallbackFactory(action="change", value=-1))
    builder.button(text="+1", callback_data=NumbersCallbackFactory(action="change", value=1))
    builder.button(text="+2", callback_data=NumbersCallbackFactory(action="change", value=2))
    builder.button(text="Подтвердить", callback_data=NumbersCallbackFactory(action="finish"))
    builder.adjust(4)
    return builder.as_markup()


async def update_numbers_text_fab(message: Message, new_value: int):
    with suppress(exceptions.TelegramBadRequest):
        await message.edit_text(
            f"Вы указали       :    {new_value}",
            reply_markup=get_numbers_keyboard_fab()
        )


@dp.callback_query(F.data == 'cmd_numerate')
async def start_cmd_numbers(callback: CallbackQuery):
    user_data[callback.from_user.id] = 0
    await callback.message.answer(text="Укажите число:    0", reply_markup=get_numbers_keyboard_fab())


@dp.callback_query(NumbersCallbackFactory.filter())
async def callbacks_numbers_change(callback: CallbackQuery, callback_data: NumbersCallbackFactory):
    print(f'INFO:получен каллбек', callback_data.__prefix__)
    user_value = user_data.get(callback.from_user.id, 0)

    if callback_data.action == "change":
        user_data[callback.from_user.id] = user_value + callback_data.value
        await update_numbers_text_fab(callback.message, user_value + callback_data.value)
    else:
        await callback.message.edit_text(f"Итого: {user_value}")
    await callback.answer()


# телеграм не позволяет боту удалить сообщения, старше определенной даты:
@dp.message(Command('clear'))
async def cmd_clear(message: Message, bot: Bot, del_forward: bool) -> None:
    # выводит "печатает" во время работы функции:
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id, interval=3.0):
        deleted_message = []
        if not del_forward:
            deleted_message = 'Функция сохранения удаляемых сообщений была отключена'
        print(f'Запрошено удаление сообщений в чате с id={message.chat.id}, в сообщении с ID = {message.message_id}')
        sum_massages, pale_messages = 0, 0
        for i in range(message.message_id, message.message_id - 5, -1):  # TODO временное значение "-5"
            try:
                if del_forward:
                    # пересылка сообщений - это "костыль", позволяющий сохранить текст сообщений:
                    ex_message = await bot.forward_message(
                        chat_id=message.chat.id,
                        from_chat_id=message.chat.id,
                        message_id=i)
                    if ex_message:
                        deleted_message.append(ex_message.text)
                        # TODO возможно, понадобиться обработка исключений, при попытке удалить старые сообщения:
                        await bot.delete_message(message.chat.id, ex_message.message_id)
                await bot.delete_message(message.chat.id, i)
            except exceptions.TelegramBadRequest:
                pale_messages += 1
            except Exception as ex:
                print(f'Выявлено исключение: {ex}')
            sum_massages += 1
        print(f'Диапазон удалений: {sum_massages}, выявлено "пустышек": {pale_messages}')
        print(f'Удалены сообщения: {deleted_message}')
        # await message.answer('/start')


@dp.callback_query(F.data == "clear")
async def clear(callback: CallbackQuery):
    await callback.answer()
    await cmd_clear(message=callback.message, bot=dp.bot, del_forward=False)


# эхо-функция
@dp.message(F.text)
async def echo_handler(message: Message) -> None:
    await message.send_copy(chat_id=message.chat.id)


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp.bot = bot
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
