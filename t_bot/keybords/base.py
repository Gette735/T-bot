from abc import ABC, abstractmethod
from aiogram.types import InlineKeyboardMarkup


class BaseKeyboard(ABC):
    @abstractmethod
    def build(self) -> InlineKeyboardMarkup:
        pass


class DynamicKeyboard(BaseKeyboard):
    """Для клавиатур, собираемых на лету"""

    def __init__(self):
        self.builder = InlineKeyboardBuilder()

    def add_button(self, text: str, callback_data: str):
        self.builder.button(text=text, callback_data=callback_data)
        return self

    def adjust(self, *args):
        self.builder.adjust(*args)
        return self

    def build(self):
        return self.builder.as_markup()