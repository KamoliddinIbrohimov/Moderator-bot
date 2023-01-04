from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from filters import IsGroup
from loader import dp


@dp.message_handler(IsGroup(), CommandHelp())
async def bot_help(message: types.Message):
    await message.answer(f"{message.from_user.full_name} Sizga qanday yordam kerak?")

