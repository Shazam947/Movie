#!/usr/bin/env python3
await message.reply_text(f"Seeked to {newpos} seconds ⏩")
except Exception as e:
await message.reply_text(f"Seek failed: {e}")


@app.on_message(filters.command("stop") & (filters.private | filters.group))
async def cmd_stop(_, message: Message):
chat_id = message.chat.id
if chat_id not in players:
await message.reply_text("Nothing to stop.")
return
try:
await pytgcalls.stop(chat_id)
except Exception:
pass
fpath = players[chat_id].get("file")
try:
if fpath and os.path.exists(fpath):
os.remove(fpath)
except Exception:
pass
players.pop(chat_id, None)
await message.reply_text("Stopped ⏹️ and cleaned up.")


@app.on_message(filters.command("status") & (filters.private | filters.group))
async def cmd_status(_, message: Message):
chat_id = message.chat.id
st = players.get(chat_id)
if not st:
await message.reply_text("No active playback.")
return
pos = st.get("position", 0)
if st.get("playing"):
pos += int(time.time() - st.get("started_at", time.time()))
await message.reply_text(f"File: {st.get('file')}\nPosition: {int(pos)} sec\nPlaying: {st.get('playing')}")


async def shutdown():
try:
await pytgcalls.stop()
except Exception:
pass
try:
await app.stop()
except Exception:
pass


async def periodic_cleanup():
while True:
try:
cleanup_temp()
except Exception:
pass
await asyncio.sleep(600)


if __name__ == "__main__":
async def main():
await app.start()
print("Userbot started. Waiting for /play commands.")
asyncio.create_task(periodic_cleanup())
from pyrogram import idle
await idle()
await shutdown()


try:
asyncio.get_event_loop().run_until_complete(main())
except KeyboardInterrupt:
print("Stopping...")
asyncio.get_event_loop().run_until_complete(shutdown())
