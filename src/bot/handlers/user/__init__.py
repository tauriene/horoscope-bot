from aiogram import Router
from .messages import msg_router
from .callbacks import cb_router

router = Router()

router.include_routers(msg_router, cb_router)
