from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def ReplyKey():
    main_key = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Catalog'), KeyboardButton(text='Back')],
            [KeyboardButton(text='Start'), KeyboardButton(text='info')]
        ],
        resize_keyboard=True,
        is_persistent = True,

    )
    return main_key