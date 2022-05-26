from pyrogram.types import Message
from asyncio import gather, sleep


async def lxme(query: str, user_id: int):
    lxmi = await arq.lxmi(query, user_id)
    return lxmi.result


async def type_and_send(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    query = message.text.strip()
    await message._client.send_chat_action(chat_id, "typing")
    response, _ = await gather(lxme(query, user_id), sleep(3))
    await message.reply_text(response)
    await message._client.send_chat_action(chat_id, "cancel")

