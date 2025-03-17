from abc import ABC, abstractmethod
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

class BaseKeyboard(ABC):
    @abstractmethod
    def build(self) -> InlineKeyboardMarkup:
        pass

class DynamicKeyboard(BaseKeyboard):
    """Для клавиатур, собираемых на лету"""

    def __init__(self):
        self.builder = InlineKeyboardBuilder()  # Используем Builder вместо Markup

    def add_button(self, text: str, callback_data: str):
        # Добавляем кнопку через метод билдера
        self.builder.button(text=text, callback_data=callback_data)
        return self

    def adjust(self, *args):
        # Настраиваем расположение кнопок
        self.builder.adjust(*args)
        return self

    def build(self) -> InlineKeyboardMarkup:
        # Преобразуем билдер в клавиатуру
        return self.builder.as_markup()