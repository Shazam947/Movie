import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped, AudioVideoPiped
from dotenv import load_dotenv
from pyrogram import idle

# Load env
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

app = Client("bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
pytgcalls = PyTgCalls(app)


@app.on_message(filters.command("play") & filters.reply)
async def play_file(_, message):
    if not message.reply_to_message:
        return await message.reply("⚠️ Reply to an audio/video file!")

    file = message.reply_to_message
    file_path = await file.download()
    chat_id = message.chat.id

    if file.video or file.document:
        stream = AudioVideoPiped(file_path)
    else:
        stream = AudioPiped(file_path)

    await pytgcalls.join_group_call(chat_id, stream)
    await message.reply("▶️ Now playing in VC!")


@app.on_message(filters.command("stop"))
async def stop(_, message):
    chat_id = message.chat.id
    await pytgcalls.leave_group_call(chat_id)
    await message.reply("⏹️ Stopped streaming.")


@app.on_message(filters.command("pause"))
async def pause(_, message):
    await pytgcalls.pause_stream(message.chat.id)
    await message.reply("⏸️ Paused.")


@app.on_message(filters.command("resume"))
async def resume(_, message):
    await pytgcalls.resume_stream(message.chat.id)
    await message.reply("▶️ Resumed.")


async def main():
    await app.start()
    await pytgcalls.start()
    print("✅ Bot is running...")
    await idle()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
