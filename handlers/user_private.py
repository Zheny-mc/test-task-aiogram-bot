from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.markdown import bold
from openpyxl import Workbook
from datetime import datetime

from common.messages import MESSAGES

user_private_router = Router()

# О боте
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(MESSAGES['start'])


# получить картинку с подписью
@user_private_router.message(Command('get_post'))
async def get_post_cmd(message: types.Message):
    file_path = './assets/logo.jpg'
    await message.answer_photo(
        photo=types.FSInputFile(path=file_path),
        caption='Добро пожаловать'
    )


# работа с гугл таблицами
@user_private_router.message(Command('work_google_table'))
async def work_google_table_cmd(message: types.Message):
    wb = Workbook()
    ws = wb.active
    ws['A2'] = 5
    wb.save('test_ex.xlsx')
    await message.answer('Ячейка A2 была заполнена 5')

# получить точку на яндекс карте
@user_private_router.message(Command('yandex_map'))
async def yandex_map_cmd(message: types.Message):
    ans_text = f'{bold("Адрес")}: площадь Ленина, 1, Санкт-Петербург, 195009'
    address = '[Открыть яндекс карты](https://yandex.ru/maps/?mode=search&text=Санкт-Петербург Ленина 1)'

    await message.answer(f"{ans_text}\n{address}", ParseMode.MARKDOWN)

# проверяю формат даты на соответствие дд.мм.гг
class AddData(StatesGroup):
    data = State()


@user_private_router.message(StateFilter(None), F.text == "/check_write_data")
async def add_data(message: types.Message, state: FSMContext):
    await message.answer('Введите дату в формате дд.мм.гггг', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddData.data)

@user_private_router.message(AddData.data, F.text)
async def check_data(message: types.Message, state: FSMContext):

    await state.update_data(name=message.text)

    vals = await state.get_data()
    input_date = vals['name']
    # проверяю формат даты на соответствие дд.мм.гг
    try:
        date_format = '%d.%m.%Y'
        datetime.strptime(input_date, date_format)
        await message.answer(f"Дата добавилась {input_date}")
    except ValueError as e:
        print(e)
        await message.answer("Дата введена неверно!")

    await state.clear()


