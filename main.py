import asyncio
from blockwatcher.subscriptions import sub_manager
from blockwatcher.database import DatabaseManager
from blockwatcher.telegram import telegram_bot_handler
from config import DB_URL

async def main():
    await telegram_bot_handler.start()
    db_manager = DatabaseManager(DB_URL)
    await db_manager.connect()
    try:
        await sub_manager(db_manager)
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user.")
    except asyncio.CancelledError:
        print("\n🛑 Task was cancelled.")
    except Exception as e:
        print(f"🛑 An error occurred: {e}")
    finally:
        await db_manager.close()

if __name__ == "__main__":
    asyncio.run(main())