import os
from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

app = Client("bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
pytgcalls = PyTgCalls(app)

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply("✅ Bot chal raha hai — /play <url> bhejo group VC me audio play karne ke liye.")

@app.on_message(filters.command("play") & filters.group)
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply("❌ Usage: `/play <direct_media_url>`")

    url = message.command[1]
    chat_id = message.chat.id

    try:
        await pytgcalls.join_group_call(
            chat_id,
            url
        )
        await message.reply(f"▶️ Playing: {url}")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

@app.on_message(filters.command("stop") & filters.group)
async def stop(_, message):
    chat_id = message.chat.id
    try:
        await pytgcalls.leave_group_call(chat_id)
        await message.reply("⏹ Stopped playback.")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

async def main():
    await app.start()
    await pytgcalls.start()
    print("🚀 Bot is running...")
    await idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
