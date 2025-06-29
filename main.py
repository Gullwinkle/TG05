import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from config import TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
API_TOKEN = TOKEN
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Создание состояний
class DateStates(StatesGroup):
    waiting_for_month = State()
    waiting_for_day = State()


def get_info(month, day):
    url = f"http://numbersapi.com/{month}/{day}/date"
    response = requests.get(url)
    return response.text

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Привет! Я бот, который расскажет тебе что произошло в этот день.\nВведите номер месяца (1-12):")
    await state.set_state(DateStates.waiting_for_month)

# Обработчик ввода месяца
@dp.message(DateStates.waiting_for_month)
async def process_month(message: Message, state: FSMContext):
    try:
        month = int(message.text)
        if 1 <= month <= 12:
            await state.update_data(month=month)
            if month in [1, 3, 5, 7, 8, 10, 12]:
                max_day = 31
            elif month == 2:
                max_day = 29
            else:
                max_day = 30
            await message.answer(f"Теперь введите число (1-{max_day}):")
            await state.update_data(max_day=max_day)
            await state.set_state(DateStates.waiting_for_day)
        else:
            await message.answer("Пожалуйста, введите число от 1 до 12.")
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число от 1 до 12.")

# Обработчик ввода дня
@dp.message(DateStates.waiting_for_day)
async def process_day(message: Message, state: FSMContext):
    user_data = await state.get_data()
    max_day = user_data.get('max_day')
    try:
        day = int(message.text)
        if 1 <= day <= max_day:
            month = user_data.get('month', '?')
            info = get_info(month, day)
            await message.answer(f"{info}")
            await state.clear()
        else:
            await message.answer(f"Пожалуйста, введите число от 1 до {max_day}.")
    except ValueError:
        await message.answer(f"Пожалуйста, введите корректное число от 1 до {max_day}.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())