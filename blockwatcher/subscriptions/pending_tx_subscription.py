import asyncio
from web3.utils.subscriptions import PendingTxSubscription
from blockwatcher.telegram import telegram_bot_handler
from blockwatcher.telegram import telegram_native_alert_handler
from blockwatcher.utils import ws_manager

async def sub_manager():
    """Sets up subscriptions for pending transactions."""
    await ws_manager.connect()

    if await ws_manager.is_connected():
        print("✅ Connected to Ethereum WebSocket!")
        w3 = ws_manager.w3

        asyncio.create_task(monitor_subscription_queue(w3))

        telegram_native_alert = PendingTxSubscription(
            label="telegram-native-alert",
            full_transactions=True,
            handler=lambda ctx: telegram_native_alert_handler(ctx, telegram_bot_handler))

        await w3.subscription_manager.subscribe([telegram_native_alert])
        await w3.subscription_manager.handle_subscriptions()
    else:
        print("❌ Connection failed. Check WSS URL.")

async def monitor_subscription_queue(w3):
    while True:
        try:
            queue = w3.provider._request_processor._handler_subscription_queue
            size = queue.qsize()
            print(f"📊 Subscription Queue Size: {size}")
        except Exception as e:
            print(f"❌ Error monitoring subscription queue: {e}")
        await asyncio.sleep(5)