from t_bot.utils.config import TOKEN_TG
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
import t_bot.keybords.factories as fact
import t_bot.keybords.keybords as kb
from t_bot.handlers.menu import menu_router
from t_bot.handlers.not_menu import not_router
from t_bot.handlers.random import random_router
from t_bot.utils.the_state_machine import StateMachine
main_state = StateMachine('main_state')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN_TG)
dp = Dispatcher()

# /start
@dp.message(Command('start'))
async def command_start(message: types.Message):
    main_state.new_state = "start"
    main_state._process()
    await message.answer(f'Привет, {message.chat.first_name}! я Тестовый бот !!!' , reply_markup = kb.ReplyKey() )

@dp.message(F.text & ~F.text.in_(["/Catalog"]) & ~F.text.in_(["/random"]))
async def echo(message: types.Message):

    if message.text == "/stop":
        await message.answer('Хорошо, заканчиваем! Держи лису')

    elif 'stop' in message.text: # Сработает на "stoppable"
        await message.answer('Хорошо, заканчиваем!')


    # В обработчике echo

    elif message.text == '/talk':
        ...
    elif message.text == '/gpt':
        ...
    elif message.text == '/quiz':
        ...
    else:
        await message.answer("Извините, это не команда")

dp.include_router(menu_router)
dp.include_router(not_router)
dp.include_router(random_router)
async def main():
    await dp.start_polling(bot)


@dp.callback_query(fact.ActionCallback.filter((F.type == "command") & (F.data == "escape")))
async def escape (callback: types.CallbackQuery):
    await callback.message.answer(f'Привет, User! я Тестовый бот !!!' )
    main_state.new_state = "start"
    main_state._process()

if __name__ == '__main__':
    asyncio.run(main())


