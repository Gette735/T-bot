import logging
from aiogram import Router, types
from aiogram.filters.command import Command

logger = logging.getLogger(__name__)
not_router = Router()  # Используем тот же роутер, что и в main.py
