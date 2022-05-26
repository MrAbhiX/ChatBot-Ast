from ChatBot import abhi, LOG_GROUP_ID as semx

async def start_bot():
    await abhi.start()
    print("[INFO]: BOT & USERBOT CLIENT STARTED !!")
    await abhi.send_message(f"{semx}", "I'm ChatBot Message Me For Chat With Me")
