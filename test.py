import asyncio
from blockwatcher.subscriptions import sub_manager
from blockwatcher.telegram import telegram_bot_handler

async def main():
    await telegram_bot_handler.start()
    try:
        await sub_manager()
    except Exception as e:
        print(f"🛑 Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())