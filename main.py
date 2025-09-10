import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from dotenv import load_dotenv

# Load .env
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

# Pyrogram client
app = Client(
    "music-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION,
)

# PyTgCalls client
call_py = PyTgCalls(app)


# ---------------- COMMAND HANDLERS ---------------- #

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("✅ Bot chal raha hai! Use /play <url>")


@app.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply("❌ URL do: `/play <yt-link or file-link>`")

    chat_id = message.chat.id
    url = message.command[1]

    try:
        await call_py.join_group_call(
            chat_id,
            AudioPiped(url)
        )
        await message.reply(f"▶️ Playing: {url}")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")


@app.on_message(filters.command("stop"))
async def stop(_, message):
    chat_id = message.chat.id
    try:
        await call_py.leave_group_call(chat_id)
        await message.reply("⏹️ Stopped playback")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")


# ---------------- MAIN ---------------- #

async def main():
    await app.start()
    await call_py.start()
    print("✅ Bot is running...")
    await idle()  # Pyrogram idle loop


if __name__ == "__main__":
    import asyncio
    from pyrogram import idle

    asyncio.get_event_loop().run_until_complete(main())
