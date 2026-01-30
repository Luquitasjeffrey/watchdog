import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendMessageRequest
import asyncio

load_dotenv()

api_id =int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
bot_username = "@lnp2pBot"
response_timeout = int(os.getenv("TIMEOUT_SECONDS", "10"))
max_attempts = int(os.getenv("ATTEMPTS_TO_REACH", "3"))
ping_interval = int(os.getenv("PING_INTERVAL_SECONDS", "60"))
chats_to_notify = [int(x) for x in os.getenv("TELEGRAM_CHATS_TO_NOTIFY", "").split(",") if x]

async def main():
    async with TelegramClient("watchdog", api_id, api_hash) as client:

        await client.start()

        response_event = asyncio.Event()

        @client.on(events.NewMessage(from_users=bot_username))
        async def handler(event):
            response_event.set()
            print("Mensaje recibido del bot: ", event.raw_text) 

        
        attempts = 0
        while True:
            await client(SendMessageRequest(bot_username, "/ping"))
            try:
                await asyncio.wait_for(response_event.wait(), timeout=response_timeout)
                attempts = 0
            except asyncio.TimeoutError:
                attempts += 1
            
                if attempts >= max_attempts:
                    for chat_id in chats_to_notify:
                        await client.send_message(chat_id, f"⚠️ No se recibió respuesta del bot {bot_username} después de {max_attempts} intentos.")
                    attempts = 0

            await asyncio.sleep(ping_interval)


asyncio.run(main())
