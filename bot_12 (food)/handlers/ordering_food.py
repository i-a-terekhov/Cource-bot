from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.simple_row import make_row_keyboard

router = Router()

# Эти значения далее будут подставляться в итоговый текст, отсюда
# такая на первый взгляд странная форма прилагательных
available_food_names = ["Суши", "Спагетти", "Хачапури"]
available_food_sizes = ["Маленькую", "Среднюю", "Большую"]

available_drinks_names = ["Кола", "Квас", "Вода"]
available_drinks_sizes = ["Маленькую", "Среднюю", "Большую"]


class OrderFood(StatesGroup):
    choosing_food_name = State()
    choosing_food_size = State()


class OrderDrink(StatesGroup):
    choosing_drink_name = State()
    choosing_drink_size = State()


@router.message(Command("food"))
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите блюдо:",
        reply_markup=make_row_keyboard(available_food_names)
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(OrderFood.choosing_food_name)

# Этап выбора блюда #


@router.message(OrderFood.choosing_food_name, F.text.in_(available_food_names))
async def food_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_food=message.text.lower())
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите размер порции:",
        reply_markup=make_row_keyboard(available_food_sizes)
    )
    await state.set_state(OrderFood.choosing_food_size)


# В целом, никто не мешает указывать стейты полностью строками
# Это может пригодиться, если по какой-то причине 
# ваши названия стейтов генерируются в рантайме (но зачем?)
@router.message(StateFilter("OrderFood:choosing_food_name"))
async def food_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого блюда.\n\n"
             "Пожалуйста, выберите одно из названий из списка ниже:",
        reply_markup=make_row_keyboard(available_food_names)
    )

# Этап выбора размера порции и отображение сводной информации #


@router.message(OrderFood.choosing_food_size, F.text.in_(available_food_sizes))
async def food_size_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_food_size=message.text.lower())
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали {user_data['chosen_food_size']} порцию {user_data['chosen_food']}.\n"
             f"Попробуйте теперь заказать напитки: /drinks",
        reply_markup=ReplyKeyboardRemove()
    )
    # Сброс состояния и сохранённых данных у пользователя (после выбора напитка, конечно)
    # await state.clear()
    await state.set_state(None)


@router.message(OrderFood.choosing_food_size)
async def food_size_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого размера порции.\n\n"
             "Пожалуйста, выберите один из вариантов из списка ниже:",
        reply_markup=make_row_keyboard(available_food_sizes)
    )

# ----------------------------------------------------------------------------------


@router.message(Command("drinks"))
async def cmd_drink(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите напиток:",
        reply_markup=make_row_keyboard(available_drinks_names)
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(OrderDrink.choosing_drink_name)


@router.message(OrderDrink.choosing_drink_name, F.text.in_(available_drinks_names))
async def drink_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_drink=message.text.lower())
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите размер стакана:",
        reply_markup=make_row_keyboard(available_drinks_sizes)
    )
    await state.set_state(OrderDrink.choosing_drink_size)


@router.message(OrderDrink.choosing_drink_name)
async def drink_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого напитка.\n\n"
             "Пожалуйста, выберите одно из названий из списка ниже:",
        reply_markup=make_row_keyboard(available_drinks_names)
    )

# Этап выбора размера стакана и отображение сводной информации #


@router.message(OrderDrink.choosing_drink_size, F.text.in_(available_drinks_sizes))
async def drink_size_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_drink_size=message.text.lower())
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали {user_data['chosen_drink_size']} объемом {user_data['chosen_drink']}.\n"
             f"Попробуйте теперь заказать еду: /food",
        reply_markup=ReplyKeyboardRemove()
    )
    # Сброс состояния и сохранённых данных у пользователя
    print(await state.get_data())
    await state.clear()


@router.message(OrderDrink.choosing_drink_size)
async def drink_size_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого размера стакана.\n\n"
             "Пожалуйста, выберите один из вариантов из списка ниже:",
        reply_markup=make_row_keyboard(available_drinks_sizes)
    )
