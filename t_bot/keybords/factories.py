from aiogram.filters.callback_data import CallbackData

# Универсальная фабрика для действий
class ActionCallback(CallbackData, prefix="action"):
    type: str   # Тип действия: "menu", "confirm", "paginate"
    data: str   # Любые данные в строке (например, "delete_user:123")

# Фабрика для пагинации
class PaginationCallback(CallbackData, prefix="page"):
    page: int
    items_per_page: int = 5