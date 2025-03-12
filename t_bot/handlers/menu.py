from .base import DynamicKeyboard
from .factories import ActionCallback

class MainMenuKeyboard(DynamicKeyboard):
    def __init__(self):
        super().__init__()
        self.add_button(
            "📁 Профиль",
            ActionCallback(type="menu", data="profile").pack()
        ).add_button(
            "⚙️ Настройки",
            ActionCallback(type="menu", data="settings").pack()
        ).adjust(1)