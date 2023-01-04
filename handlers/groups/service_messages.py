import asyncio

from aiogram import types

from filters import IsGroup
from loader import dp, bot


@dp.message_handler(IsGroup(), content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member(message: types.Message):
    member = ", ".join([m.get_mention(as_html=True) for m in message.new_chat_members])
    msg = await message.reply(f"Xush kelibsiz {member}")
    await asyncio.sleep(5)
    await message.delete()
    await msg.delete()


@dp.message_handler(IsGroup(), content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def left_member(message: types.Message):
    if message.left_chat_member.id == message.from_user.id:
        msg = await message.answer(f"{message.left_chat_member.get_mention(as_html=True)} guruhni tark etdi")
        await asyncio.sleep(5)
        await message.delete()
        await msg.delete()
    elif message.left_chat_member.id == (await bot.me).id:
        return
    else:
        msg = await message.answer(f"{message.left_chat_member.full_name} guruhdan haydaldi\n"
                             f"Admin: {message.from_user.get_mention(as_html=True)}.")
        await asyncio.sleep(5)
        await message.delete()
        await msg.delete()