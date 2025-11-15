import asyncio
from web3.utils.subscriptions import PendingTxSubscription
from blockwatcher.telegram import telegram_bot_handler
from blockwatcher.telegram import telegram_native_alert_handler, telegram_erc20_alert_handler
from blockwatcher.utils import ws_manager

async def run_subscription(label, handler, telegram_bot_handler, db_manager):
    """Run a single subscription."""
    w3 = ws_manager.w3
    subscription = PendingTxSubscription(
        label=label,
        full_transactions=True,
        handler=lambda ctx: handler(ctx, telegram_bot_handler, db_manager)
    )
    await w3.subscription_manager.subscribe([subscription])
    await w3.subscription_manager.handle_subscriptions()

async def sub_manager(db_manager):
    """Sets up subscriptions for pending transactions."""
    await ws_manager.connect()

    if await ws_manager.is_connected():
        print("✅ Connected to Ethereum WebSocket!")

        asyncio.create_task(monitor_subscription_queue(ws_manager.w3))

        tasks = [
            asyncio.create_task(run_subscription("telegram-native-alert", telegram_native_alert_handler, telegram_bot_handler, db_manager)),
            asyncio.create_task(run_subscription("telegram-erc20-alert", telegram_erc20_alert_handler, telegram_bot_handler, db_manager))
        ]

        await asyncio.gather(*tasks)
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