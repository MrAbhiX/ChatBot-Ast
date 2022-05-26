from pyrogram.types import Message
from pyrogram import filters
from ChatBot.Database.Mongo import db
from ChatBot.Database import (db,
                              check_chatbot, 
                              add_chatbot, 
                              rm_chatbot,
                              chatbot_group,
                              
                              )
from ChatBot.Helpers import capture_error



async def chat_bot_toggle(message: Message, is_userbot: bool):
    status = message.text.split(None, 1)[1].lower()
    chat_id = message.chat.id
    db = await check_chatbot()
    db = db["userbot"] if is_userbot else db["bot"]
    if status == "enable":
        if chat_id not in db:
            await add_chatbot(chat_id, is_userbot=is_userbot)
            text = "Chatbot Enabled!"
            return await eor(message, text=text)
        await eor(message, text="ChatBot Is Already Enabled.")
    elif status == "disable":
        if chat_id in db:
            await rm_chatbot(chat_id, is_userbot=is_userbot)
            return await eor(message, text="Chatbot Disabled!")
        await eor(message, text="ChatBot Is Already Disabled.")
    else:
        await eor(message, text="**Usage:**\n/chatbot [ENABLE|DISABLE]")


# Enabled | Disable Chatbot



async def type_and_send(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    query = message.text.strip()
    await message._client.send_chat_action(chat_id, "typing")
    response, _ = await gather(lunaQuery(query, user_id), sleep(3))
    await message.reply_text(response)
    await message._client.send_chat_action(chat_id, "cancel")





# FOR USERBOT


@abhi.on_message(
    filters.command("chatbot", prefixes=USERBOT_PREFIX)
    & ~filters.edited
    & SUDOERS
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
