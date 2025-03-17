from t_bot.utils.gpt_service import ChatGPTService as ChatGpt
from t_bot.utils.the_state_machine import StateMachine
from t_bot.keybords.base import DynamicKeyboard as kb
import t_bot.keybords.factories as fact
from aiogram import Router, types, F
from aiogram.filters import Command
import hashlib
import time
import logging
quiz_router = Router()
logger = logging.getLogger(__name__)
quiz_state = StateMachine('quiz')
quiz_state.new_state = 'idle'
cache = {}
quiz_gpt = ChatGpt()
import asyncio
quiz_gpt.set_system_message('''You are questmaster. Ask user a question and give him four variants of answer. '
                            'Give him the answer in listcle. Get the answer as a number of one of your answers.'
                            ' Use russian language in your answer. '
                            'Format: "question + four answer:'
                            'Question: [Your question]'
                            1. [answer], 2. [answer],
                            3. [answer], 4. [answer],
                            "'''
                            )


def get_navigation_path_quiz() -> list:
    if ':' in quiz_state.current_state:
        return quiz_state.current_state.split(':')[1:]
    return []


def update_navigation_quiz(new_step: str):
    base_state = quiz_state.current_state.split(':')[0] if ':' in quiz_state.current_state else quiz_state.current_state
    quiz_state.new_state = f"{base_state}:{new_step}"
    quiz_state._process()

@quiz_router.message(Command('/quiz'))
async def greet_message_quiz(message: types.Message):
    if quiz_state.current_state == 'idle':
        quiz_state.new_state = "in_action"
        quiz_state._process()
        logger.info('Quiz is activated')
        quiz_kb =kb()
        greet_text = (f'Hi, {message.chat.first_name}!!!')

        quiz_kb.add_button(
            text='Start',
            callback_data = fact.ActionCallback(type="command", data="quiz_1").pack()
        )
        quiz_kb.add_button(
            text='Escape',
            callback_data=fact.ActionCallback(type="command", data="escape").pack()
        )
        await message.answer(greet_text, reply_markup=quiz_kb.build())
    else:
        await message.answer('Something went wrong. Please try again later')
        logger.warning(f"Quiz activation failed. Current state: {quiz_state.current_state}")

@quiz_router.callback_query(fact.ActionCallback.filter((F.type == "command") & (F.data == "quiz_1")))
async def greet_callback_quiz(callback: types.CallbackQuery, callback_data: fact.ActionCallback):
    if quiz_state.current_state == 'idle' or quiz_state.current_state == 'in_action':
        quiz_state.new_state = "in_action"
        quiz_state._process()
        logger.info('Quiz is activated')
        quiz_kb =kb()
        greet_text = ('We\'re starting quiz!!!')

        quiz_kb.add_button(
            text='Start',
            callback_data = fact.ActionCallback(type="command", data="start_quiz").pack()
        )
        quiz_kb.add_button(
            text='Escape',
            callback_data=fact.ActionCallback(type="command", data="escape").pack()
        )
        await callback.answer.edit_text(greet_text, reply_markup=quiz_kb.build())
        await callback.answer()
    else:
        await callback.message.edit_text('Something went wrong. Please try again later')
        logger.warning(f"Quiz activation failed. Current state: {quiz_state.current_state}")

@quiz_router.callback_query(fact.ActionCallback.filter((F.type=="command")&(F.data == "start_quiz")))
async def quiz_choose(callback: types.CallbackQuery, callback_data: fact.ActionCallback):
    if quiz_state.current_state == 'in_action':
        quiz_kb = kb()
        choose_text = ('Please choose the topic!!!')
        quiz_kb.add_button(
            text='Cosmos',
            callback_data=fact.ActionCallback(type="command", data="start_cosmos").pack()
        )
        quiz_kb.add_button(
            text='History',
            callback_data=fact.ActionCallback(type="command", data="start_history").pack()
        )
        quiz_kb.add_button(
            text='Science',
            callback_data=fact.ActionCallback(type="command", data="start_science").pack()
        )

        quiz_kb.add_button(
            text='Escape',
            callback_data=fact.ActionCallback(type="command", data="escape").pack()
        )
        await callback.answer.edit_text(choose_text, reply_markup=quiz_kb.build())
        await callback.answer()
    else:
        await callback.message.edit_text('Something went wrong. Please try again later')
        logger.warning(f"Quiz activation failed. Current state: {quiz_state.current_state}")


@quiz_router.callback_query(fact.ActionCallback.filter((F.type == "command") & (F.data == "start_cosmos")))
async def handle_cosmos_quiz(callback: types.CallbackQuery, callback_data: fact.ActionCallback):
    if quiz_state.current_state == 'in_action':
        try:
            # Generate question
            quiz_gpt.add_user_message("Generate one cosmic question with 4 options")
            question = await asyncio.to_thread(quiz_gpt.get_response)

            # Store question and extract answer
            parts = [line.strip() for line in question.split('\n') if line.strip()]
            question_text = parts[0].replace("Question:", "").strip()
            cache[callback.from_user.id] = {
                'question': question_text,
                'correct': next(i + 1 for i, p in enumerate(parts) if "[correct]" in p.lower())
            }

            # Build interface
            quiz_kb = kb()
            for i in range(4):
                quiz_kb.add_button(
                    text=f"{i + 1}️⃣",
                    callback_data=fact.ActionCallback(type="answer", data=str(i + 1)).pack()
                )
            quiz_kb.add_button(
                text="🏁 Finish",
                callback_data=fact.ActionCallback(type="command", data="finish").pack()
            )

            await callback.message.edit_text(
                f"🌌 *Cosmic Challenge:*\n{question_text}",
                reply_markup=quiz_kb.build(),
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Cosmos error: {str(e)}")
            await callback.message.edit_text("System malfunction")
            quiz_state.new_state = "idle"


@quiz_router.callback_query(fact.ActionCallback.filter(F.type == "answer"))
async def handle_answer(callback: types.CallbackQuery):
    try:
        user_data = cache.get(callback.from_user.id, {})
        selected = int(callback.data)

        if not user_data:
            raise ValueError("No session data")

        result = "✅ Correct!" if selected == user_data['correct'] else "❌ Wrong"
        await callback.message.edit_text(
            f"🚀 *Result:* {result}\n"
            f"📝 Question: {user_data['question']}\n"
            f"🔢 Your choice: {selected}",
            parse_mode="Markdown"
        )
        quiz_state.new_state = "idle"
    except Exception as e:
        logger.error(f"Answer error: {str(e)}")
        await callback.answer("⚠️ Processing error")


@quiz_router.callback_query(fact.ActionCallback.filter(F.data == "finish"))
async def final_determination(callback: types.CallbackQuery):
    await callback.message.edit_text("🎉 *Quiz Completed!*\n"
                                     "Type /quiz to restart",
                                     parse_mode="Markdown")
    quiz_state.new_state = "idle"
    cache.pop(callback.from_user.id, None)