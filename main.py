import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioStream, InputVideoStream
from pytgcalls.types.input_stream.quality import MediumAudioQuality, MediumVideoQuality
from pytgcalls.types import AudioVideoPiped
from dotenv import load_dotenv

# Load env
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

app = Client("bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
pytgcalls = PyTgCalls(app)


@app.on_message(filters.command("play") & filters.reply)
async def play_file(_, message):
    if not message.reply_to_message or not message.reply_to_message.video and not message.reply_to_message.document:
        return await message.reply("Reply to a video or audio file!")

    file_path = await message.reply_to_message.download()
    chat_id = message.chat.id

    await pytgcalls.join_group_call(
        chat_id,
        AudioVideoPiped(
            file_path,
            audio_parameters=MediumAudioQuality(),
            video_parameters=MediumVideoQuality(),
        ),
    )
    await message.reply("▶️ Playing in VC!")


@app.on_message(filters.command("stop"))
async def stop(_, message):
    chat_id = message.chat.id
    await pytgcalls.leave_group_call(chat_id)
    await message.reply("⏹️ Stopped streaming.")


@app.on_message(filters.command("pause"))
async def pause(_, message):
    chat_id = message.chat.id
    await pytgcalls.pause_stream(chat_id)
    await message.reply("⏸️ Paused.")


@app.on_message(filters.command("resume"))
async def resume(_, message):
    chat_id = message.chat.id
    await pytgcalls.resume_stream(chat_id)
    await message.reply("▶️ Resumed.")


async def main():
    await app.start()
    await pytgcalls.start()
    print("Bot is running...")
    await idle()


if __name__ == "__main__":
    import asyncio
    from pyrogram import idle

    asyncio.run(main())
