# handlers/errors.py
import logging
from aiogram import Router
from aiogram.types import ErrorEvent

logger = logging.getLogger(__name__)
error_router = Router()  # Переименовали переменную router в error_router

@error_router.errors()
async def error_handler(event: ErrorEvent):
    """
    Обработчик всех ошибок
    """
    logger.error(
        f"Произошла ошибка: {event.exception} \nв обновлении: {event.update}"
    )

def register_error_handler(router: Router) -> None:
    """
    Регистрирует обработчик ошибок
    """
    router.include_router(error_router)  # Используем error_router вместо router
