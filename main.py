import asyncio
from blockwatcher.subscriptions.pending_tx_subscription import sub_manager
from blockwatcher.database.db_manager import DatabaseManager
from config import DB_URL

async def main():
    db_manager = DatabaseManager(DB_URL)
    await db_manager.connect()
    await db_manager.create_tables()
    try:
        await sub_manager(db_manager)
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user.")
    except asyncio.CancelledError:
        print("\n⚠️ Task was cancelled.")
    except Exception as e:
        print(f"⚠️ An error occurred: {e}")
    finally:
        await db_manager.close()
    
if __name__ == "__main__":
    asyncio.run(main())