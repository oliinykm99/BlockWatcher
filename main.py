import asyncio
from blockwatcher.subscriptions.pending_tx_subscription import sub_manager

async def main():
    """Main entry point for the BlockWatcher application."""
    await sub_manager()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user.")
    except Exception as e:
        print(f"⚠️ An error occurred: {e}")