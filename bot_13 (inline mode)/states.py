from aiogram.fsm.state import StatesGroup, State


# 'Ожидает ввод'
class SaveCommon(StatesGroup):
    waiting_for_save_start = State()


# 'ожидает ввод заголовка' и 'ожидает ввод описания'
class TextSave(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()


class DeleteCommon(StatesGroup):
    waiting_for_delete_start = State()



