from telegram_listener import client

async def main():
    await client.start()
    print("Listening for messages...")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())
