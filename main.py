import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputAudioStream

# apna config set karo
API_ID = int("29684831")
API_HASH = "33c51717f00a7b7431dbc8e1894c8d58"
SESSION = "BQE1hZwAUsUKRBkYc-addSD1ayxFN62wXdd-xPbtqDRGyPVgS67h2fskzr4V-xTyUBL1FJzgnHjKQi0O5RvZ7dq7NU4QT78fnJQAiweGQ0OP0pk4vh44I5nRALuUjR8EuZHsBG798UMJhv5U8_YOSxjG5ue4PkVHQgb2Ug86pd8KXaoDK6gx2kdXxNfc2jXlg4EjlQy4A3welIRsfytI0D5H9q4HuRMrcJ5VmkTE8-u4IoO0__DOWX1RADzLfXjSTi9rzFbR6nyjY0mhM7eDF1hM24_EoBMGUMmTKzPCemJdEdBfkHr05DUKzLS-fOqpZYMOhJ93NxTmo7RGQDbvRfgl8V6phQAAAAHhdxYfAA"

app = Client(SESSION, api_id=API_ID, api_hash=API_HASH)
pytgcalls = PyTgCalls(app)


# 🔹 join + play
@app.on_message(filters.command("play") & filters.me)
async def play_handler(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: /play filename.mp3")

    file = message.command[1]
    chat_id = message.chat.id

    await pytgcalls.join_group_call(
        chat_id,
        InputStream(
            InputAudioStream(
                file,
            )
        ),
    )
    await message.reply(f"▶️ Playing: {file}")


# 🔹 pause
@app.on_message(filters.command("pause") & filters.me)
async def pause_handler(client, message):
    await pytgcalls.pause_stream(message.chat.id)
    await message.reply("⏸ Paused")


# 🔹 resume
@app.on_message(filters.command("resume") & filters.me)
async def resume_handler(client, message):
    await pytgcalls.resume_stream(message.chat.id)
    await message.reply("▶️ Resumed")


# 🔹 skip (basically change track)
@app.on_message(filters.command("skip") & filters.me)
async def skip_handler(client, message):
    await pytgcalls.leave_group_call(message.chat.id)
    await message.reply("⏭ Skipped")


# 🔹 stop
@app.on_message(filters.command("stop") & filters.me)
async def stop_handler(client, message):
    await pytgcalls.leave_group_call(message.chat.id)
    await message.reply("⏹ Stopped")


# run
async def main():
    await app.start()
    await pytgcalls.start()
    print("✅ Bot is running...")
    await idle()
    await app.stop()


if __name__ == "__main__":
    asyncio.run(main())
