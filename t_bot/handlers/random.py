from t_bot.utils.gpt_service import ChatGPTService as GPT
from aiogram import Router, types, F
from aiogram.filters import Command
from t_bot.keybords.base import DynamicKeyboard as KB
import t_bot.keybords.factories as fact
from t_bot.utils.the_state_machine import StateMachine
import hashlib
import time
import logging

random_router = Router()
logger = logging.getLogger(__name__)

random_state = StateMachine('random')
cache = {}
random_gpt = GPT()

random_gpt.set_system_message('Provide random facts in 1-2 sentences.Use russian language in your answer. Format: "Fact: [content] • Source: [topic]"')

@random_router.message(Command('random'))
async def random_handler(message: types.Message):
    random_state.new_state = "active"
    random_state._process()
    try:
        response = random_gpt.get_response(prompt="Generate random fact", model="gpt-3.5-turbo", temperature=0.9)
    except Exception as e:
        logger.error(f"GPT Error: {e}")
        response = "Service unavailable"

    menu = KB()
    menu.add_button("Get Fact", fact.ActionCallback(type="cmd", data="fact").pack())
    menu.add_button("Exit", fact.ActionCallback(type="cmd", data="exit").pack())

    await message.answer("Menu:", reply_markup=menu.build())

@random_router.callback_query(fact.ActionCallback.filter(F.type == "cmd"))
async def fact_handler(callback: types.CallbackQuery, callback_data: fact.ActionCallback):
    if callback_data.data != "fact":
        return

    uid = f"{callback.from_user.id}_{callback.message.message_id}"
    hash_key = hashlib.md5(f"{uid}_{time.time()}".encode()).hexdigest()

    if cache.get(uid) == hash_key:
        await callback.answer()
        return

    try:
        response = random_gpt.get_response(prompt="Generate random fact", model="gpt-3.5-turbo", temperature=0.9)
    except Exception as e:
        logger.error(f"GPT Error: {e}")
        response = "Service unavailable"

    random_menu = KB()
    random_menu.add_button("New Fact", fact.ActionCallback(type="cmd", data=f"fact_{hash_key}").pack())
    random_menu.add_button("Escape", fact.ActionCallback(type="command", data='escape').pack())

    try:
        await callback.message.edit_text(response, reply_markup=random_menu.build())
        cache[uid] = hash_key
    except Exception as e:
        logger.error(f"Edit Error: {e}")

    await callback.answer()

