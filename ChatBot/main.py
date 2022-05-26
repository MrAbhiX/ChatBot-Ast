from pyrogram import Client, filters, idle
import aiohttp
from Python_ARQ import ARQ
from os import environ, getenv
from inspect import getfullargspec
from asyncio import get_event_loop
from pyrogram.types import Message

LOG_GROUP_ID = int(environ.get("LOG_GROUP_ID", None))
API_ID = int(environ.get("API_ID", 6))
API_HASH = environ.get("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
SESSION_NAME = environ.get("SESSION_NAME", None)
USERBOT_PREFIX = environ.get("USERBOT_PREFIX", ".")
MONGO_URL = environ.get("MONGO_URL", None)
ARQ_API_URL = environ.get("ARQ_API_URL", None)
ARQ_API_KEY = environ.get("ARQ_API_KEY", None)
USERBOT_ID = int(getenv("USERBOT_ID", "")
USERBOT_USERNAME = getenv("USERBOT_USERNAME", "")

abhi = Client(
    api_id=API_ID,
    api_hash=API_HASH,
    session_name=SESSION_NAME,
    plugins=dict(root="ChatBot.Plugins")
    )
    



with abhi as app:
    lakshu = abhi.get_me()

USERBOT_ID = lakshu.id
USERBOT_NAME = lakshu.first_name + (lakshu.last_name or "")
USERBOT_USERNAME = lakshu.username
USERBOT_MENTION = lakshu.mention
USERBOT_DC_ID = lakshu.dc_id
SUDOERS = filters.user()


if USERBOT_ID not in SUDOERS:
    SUDOERS.add(USERBOT_ID)
    

        
async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})


async def main():
    global arq
    session = aiohttp.ClientSession()
    arq = ARQ(ARQ_API_URL, ARQ_API_KEY, session)

    await abhi.start()
    await abhi.send_message(LOG_GROUP_ID, "I'm ChatBot Message Me For Chat With Me")
    print(
        """
-----------------
| ChatBot Assistant Started Made By Abhi! |
-----------------
"""
    )
    await idle()


loop = get_event_loop()
loop.run_until_complete(main())
