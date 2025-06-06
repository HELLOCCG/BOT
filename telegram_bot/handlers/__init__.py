from aiogram import Router
from .callbacks import router as callbacks_router

def register_all_handlers(router: Router) -> None:
    """Регистрирует все обработчики"""
    router.include_router(callbacks_router)
