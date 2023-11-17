from asyncio import sleep
from pprint import pprint

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.checkin import get_checkin_kb
from middlewares.long_operation import ChatActionMiddleware

router = Router()
router.message.middleware(ChatActionMiddleware())


@router.message(Command("checkin"), flags={"long_operation": "typing"})
async def cmd_checkin(message: Message):
    await sleep(10)
    await message.answer(
        "Пожалуйста, нажмите на кнопку ниже:",
        reply_markup=get_checkin_kb()
    )


@router.callback_query(F.data == "confirm", flags={"long_operation": "typing"})
async def checkin_confirm(callback: CallbackQuery):
    await sleep(3)
    pprint(callback.message)
    await callback.answer(
        "Спасибо, подтверждено!",
        show_alert=True
    )

