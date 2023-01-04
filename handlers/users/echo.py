import asyncio

from aiogram import types
from filters import IsPrivate
from loader import dp
import logging

# Echo bot
@dp.message_handler(IsPrivate(), state=None)
async def bot_echo(message: types.Message):
    logging.info(message)
    ms = await message.answer(f"{message.from_user.full_name} Siz noto'g'ri kamanda kiritdinggiz\n"
                              f"iltimos tekshirib qayta kamanda kiriting")
#   await message.reply_to_message.delete()
    await message.delete()
    await asyncio.sleep(5)
    await ms.delete()

