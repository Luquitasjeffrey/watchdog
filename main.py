import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendMessageRequest
import asyncio

load_dotenv()

api_id =int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
bot_username = "@lnp2pBot"
TIMEOUT = 10  # segundos

client = TelegramClient("watchdog", api_id, api_hash)

async def main():
    await client.start()

    response_event = asyncio.Event()

    @client.on(events.NewMessage(from_users=bot_username))
    async def handler(event):
        if "pong" in event.raw_text.lower():
            response_event.set()
        else:
            print("Mensaje recibido del bot, pero no es una respuesta válida:", event.raw_text) 

    await client(SendMessageRequest(bot_username, "/ping"))

    try:
        await asyncio.wait_for(response_event.wait(), timeout=TIMEOUT)
        print("OK: el bot respondió /ping")
    except asyncio.TimeoutError:
        print("FAIL: el bot NO respondió /ping")

    await client.disconnect()

asyncio.run(main())
