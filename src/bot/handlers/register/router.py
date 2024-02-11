from aiogram import Router

from src.bot.filters.register import RegisterFilter

router = Router()
router.message.filter(RegisterFilter())
