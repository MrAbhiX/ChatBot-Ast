from asyncio import gather, sleep
import aiohttp
from pyrogram import filters
from pyrogram.types import Message

from ChatBot.Database import (
                              check_chatbot, 
                              add_chatbot, 
                              rm_chatbot,
                              chatbot_group)
from ChatBot.Helpers import (capture_error,
                             chat_bot_toggle,
                             type_and_send)

from ChatBot.main import (abhi, 
                          
                          USERBOT_PREFIX,
                          USERBOT_ID,
                          USERBOT_USERNAME)
                  
from inspect import getfullargspec    
                          

from ChatBot.Database.Mongo import db
from ChatBot.Database.functions import chatbotdb

session = aiohttp.ClientSession()
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, session)

async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})



@abhi.on_message(
    filters.command("chatbot", prefixes=USERBOT_PREFIX)
    & ~filters.edited
    & filters.user
)
@capture_error
async def chatbot_status_ubot(_, message: Message):
    if len(message.text.split()) != 2:
        return await eor(message, text="**Usage:**\n.chatbot [ENABLE|DISABLE]")
    await chat_bot_toggle(message, is_userbot=True)


@abhi.on_message(
    ~filters.me & ~filters.private & filters.text & ~filters.edited,
    group=chatbot_group,
)
@capture_error
async def chatbot_talk_ubot(_, message: Message):
    db = await check_chatbot()
    if message.chat.id not in db["userbot"]:
        return
    username = "@" + str(USERBOT_USERNAME)
    if message.reply_to_message:
        if not message.reply_to_message.from_user:
            return
        if (
                message.reply_to_message.from_user.id != USERBOT_ID
                and username not in message.text
        ):
            return
    else:
        if username not in message.text:
            return
    await type_and_send(message)


@abhi.on_message(
    filters.text & filters.private & ~filters.me & ~filters.edited,
    group=(chatbot_group + 1),
)
@capture_error
async def chatbot_talk_ubot_pm(_, message: Message):
    db = await check_chatbot()
    if message.chat.id not in db["userbot"]:
        return
    await type_and_send(message)
