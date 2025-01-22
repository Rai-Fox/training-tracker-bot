from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from utils import get_help_message, get_start_message

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.reply(get_start_message())


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.reply(get_help_message())
