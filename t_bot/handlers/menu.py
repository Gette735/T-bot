from aiogram import Router, F, types
from aiogram.filters import Command
import t_bot.keybords.base as base
import t_bot.keybords.factories as fact
import logging

menu_router = Router()
logger = logging.getLogger(__name__)
from t_bot.utils.the_state_machine import StateMachine

menu_state = StateMachine('menu_state')


def get_navigation_path() -> list:
    if ':' in menu_state.current_state:
        return menu_state.current_state.split(':')[1:]
    return []


def update_navigation(new_step: str):
    base_state = menu_state.current_state.split(':')[0] if ':' in menu_state.current_state else menu_state.current_state
    menu_state.new_state = f"{base_state}:{new_step}"
    menu_state._process()


@menu_router.message(F.text == "/Catalog")
async def build_catalog_keyboard(message: types.Message):
    logger.info("Catalog вызван")
    menu_state.new_state = "base_catalog"
    menu_state._process()

    keyboard = base.DynamicKeyboard()
    keyboard.add_button(
        text="Fox Subcatalog",
        callback_data=fact.ActionCallback(type="subcatalog", data="fox_1").pack()
    )
    keyboard.add_button(
        text="AI Subcatalog",
        callback_data=fact.ActionCallback(type="subcatalog", data="ai_1").pack()
    )
    keyboard.add_button(
        text="Simple Subcatalog",
        callback_data=fact.ActionCallback(type="subcatalog", data="simple_1").pack()
    )
    keyboard.adjust(2)
    await message.answer("Choose the subcatalog:", reply_markup=keyboard.build())


@menu_router.callback_query(fact.ActionCallback.filter(F.type == "subcatalog"))
async def handle_subcatalog(callback: types.CallbackQuery, callback_data: fact.ActionCallback):
    if callback_data.data == "fox_1":
        update_navigation("fox_1")
        keyboard = base.DynamicKeyboard()
        logger.info("Catalog 'Fox' вызван")
        keyboard.add_button(
            text="Fox Subcatalog 2️⃣",
            callback_data=fact.ActionCallback(type="subcatalog", data="fox_2").pack()
        )
        await callback.message.edit_text("Subcatalog 1:", reply_markup=keyboard.build())

    elif callback_data.data == "simple_1":
        update_navigation("simple_1")
        keyboard = base.DynamicKeyboard()
        logger.info("Catalog 'Simple' вызван")
        keyboard.add_button(
            text="Quiz",
            callback_data=fact.ActionCallback(type="command", data="quiz_1").pack()
        )
        keyboard.add_button(
            text="Random",
            callback_data=fact.ActionCallback(type="subcatalog", data="random_1").pack()
        )
        await callback.message.edit_text("Subcatalog 'AI':", reply_markup=keyboard.build())

    elif callback_data.data == "ai_1":
        update_navigation("ai_1")
        keyboard = base.DynamicKeyboard()
        logger.info("Catalog 'AI' вызван")
        keyboard.add_button(
            text="Talking to a famous man.",
            callback_data=fact.ActionCallback(type="subcatalog", data="talk_1").pack()
        )
        keyboard.add_button(
            text="ChatGPT",
            callback_data=fact.ActionCallback(type="subcatalog", data="gpt_talk_1").pack()
        )
        await callback.message.edit_text("Subcatalog 'Simple':", reply_markup=keyboard.build())

    elif callback_data.data == "talk_1":
        update_navigation("talk_1")
        logger.info("Catalog 'Talk' вызван")
        keyboard = base.DynamicKeyboard()
        keyboard.add_button(
            text="🦊",
            callback_data=fact.ActionCallback(type="function", data="fox_final").pack()
        )
        await callback.message.edit_text("Subcatalog 2:", reply_markup=keyboard.build())

    elif callback_data.data == "fox_2":
        update_navigation("fox_2")
        keyboard = base.DynamicKeyboard()
        keyboard.add_button(
            text="🦊",
            callback_data=fact.ActionCallback(type="function", data="fox_final").pack()
        )
        await callback.message.edit_text("Subcatalog 2:", reply_markup=keyboard.build())


@menu_router.callback_query(fact.ActionCallback.filter((F.type == "function") & (F.data == "fox_final")))
async def fox_final(callback: types.CallbackQuery):
    await callback.message.answer("🦊")
    # Полный сброс навигации
    menu_state.new_state = "base_catalog"
    menu_state._process()