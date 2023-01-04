import asyncio
import datetime
import re

import aiogram
from aiogram import types
from aiogram.dispatcher.filters import Command, Text, Regexp
from aiogram.utils.exceptions import BadRequest

from filters import IsGroup, AdminFilter
from loader import dp, bot


# /ro oki !ro (read-only) komandalari uchun handler
# foydalanuvchini read-only ya'ni faqat o'qish rejimiga o'tkazib qo'yamiz.
@dp.message_handler(IsGroup(), Command("ro", prefixes="!/"), AdminFilter())
async def read_only_mode(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    command_parse = re.compile(r"(!ro|/ro) ?(\d+)? ?([\w+\D]+)?")
    parsed = command_parse.match(message.text)
    time = parsed.group(2)
    comment = parsed.group(3)
    if not time:
        time = 5

    """
    !ro 
    !ro 5 
    !ro 5 test
    !ro test
    !ro test test test
    /ro 
    /ro 5 
    /ro 5 test
    /ro test
    """
    # 5-minutga izohsiz cheklash
    # !ro 5
    # command='!ro' time='5' comment=[]

    # 50 minutga izoh bilan cheklash
    # !ro 50 reklama uchun ban
    # command='!ro' time='50' comment=['reklama', 'uchun', 'ban']

    time = int(time)

    # Ban vaqtini hisoblaymiz (hozirgi vaqt + n minut)
    until_date = datetime.datetime.now() + datetime.timedelta(minutes=time)

    try:
        await message.chat.restrict(user_id=member_id, can_send_messages=False, until_date=until_date)
        await message.reply_to_message.delete()
    except aiogram.utils.exceptions.BadRequest as err:
        msg = await message.answer(f"Xatolik! {err.args}")
        await message.delete()
        await asyncio.sleep(5)
        await msg.delete()
        return

    # Пишем в чат
    msg = await message.answer(
        f"Foydalanuvchi {message.reply_to_message.from_user.full_name} {time} minut yozish huquqidan mahrum qilindi.\n"
        f"Sabab: \n<b>{comment}</b>")

    await message.delete()
    await asyncio.sleep(30)
    await msg.delete()


# gruhdagi reklamalarni taqiqlash
Link = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)'
Email = r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+'


@dp.message_handler(IsGroup(), Regexp(Email))
@dp.message_handler(IsGroup(), Regexp(Link))
async def ro_advertising(message: types.Message):
    member = message.from_user
    member_id = member.id
    chat_id = message.chat.id
    # time = 10
    # comment = "Reklama tarqatdi"
    # until_date = datetime.datetime.now() + datetime.timedelta(minutes=time)
    try:
        await message.delete()
        msg = await message.answer(f"👮‍ {message.from_user.get_mention(as_html=True)} gruxda reklama tarqatmang🚫")
        await asyncio.sleep(10)
        await msg.delete()
        # await message.chat.restrict(user_id=member_id, can_send_messages=False, until_date=until_date)
        # await message.delete()
        # msg = await message.answer(
        #     f"Foydalanuvchi {message.from_user.full_name} {time} minut yozish huquqidan mahrum qilindi.\n"
        #     f"Sabab: <b>{comment}</b>")
        # await asyncio.sleep(10)
        # await msg.delete()
    except aiogram.utils.exceptions.BadRequest:
        return



# read-only holatdan qayta tiklaymiz
@dp.message_handler(IsGroup(), Command("unro", prefixes="!/"), AdminFilter())
async def undo_read_only_mode(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id

    user_allowed = types.ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_invite_users=True,
        can_change_info=False,
        can_pin_messages=False,
    )
    service_message = await message.reply("Xabar 5 sekunddan so'ng o'chib ketadi.")

    await asyncio.sleep(5)
    await message.chat.restrict(user_id=member_id, permissions=user_allowed, until_date=0)
    await message.reply(f"Foydalanuvchi {member.full_name} tiklandi")

    # xabarlarni o'chiramiz
    await message.delete()
    await service_message.delete()


# Foydalanuvchini banga yuborish (guruhdan haydash)
@dp.message_handler(IsGroup(), Command("ban", prefixes="!/"), AdminFilter())
async def ban_user(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    await message.chat.kick(user_id=member_id)

    await message.answer(f"Foydalanuvchi {message.reply_to_message.from_user.full_name} guruhdan haydaldi")

    await asyncio.sleep(5)
    await message.delete()


# Foydalanuvchini bandan chiqarish, foydalanuvchini guruhga qo'sha olmaymiz (o'zi qo'shilishi mumkin)
@dp.message_handler(IsGroup(), Command("unban", prefixes="!/"), AdminFilter())
async def unban_user(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id
    await message.chat.unban(user_id=member_id)
    await message.answer(f"Foydalanuvchi {message.reply_to_message.from_user.full_name} bandan chiqarildi")

    await asyncio.sleep(5)

    await message.delete()


@dp.message_handler(IsGroup(), Command("unr", prefixes="!/"), AdminFilter())
async def undo_read_only_mode(message: types.Message):
    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id

    user_allowed = types.ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=False,
        can_send_polls=False,
        can_send_other_messages=False,
    )
    service_message = await message.reply("Xabar 5 sekunddan so'ng o'chib ketadi.")

    await asyncio.sleep(5)
    await message.chat.restrict(user_id=member_id, permissions=user_allowed, until_date=0)
    await message.reply(f"Foydalanuvchi {member.full_name} tiklandi")

    # xabarlarni o'chiramiz
    await message.delete()
    await service_message.delete()
    await message.reply_to_message.delete()
