import asyncio
import logging
from web3.utils.subscriptions import PendingTxSubscription
from blockwatcher.handlers import kafka_pending_native_tx_handler, kafka_pending_erc20_tx_handler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def run_subscription(label, handler, ws_manager, kafka_producer=None, rpc_manager=None):
    """Run a single subscription."""
    w3 = ws_manager.w3
    subscription = PendingTxSubscription(
        label=label,
        full_transactions=True,
        handler=lambda ctx: handler(ctx, kafka_producer, rpc_manager)
    )
    await w3.subscription_manager.subscribe([subscription])
    await w3.subscription_manager.handle_subscriptions()

async def sub_manager(kafka_producer, ws_manager, rpc_manager):
    """Sets up subscriptions for pending transactions."""
    if await ws_manager.is_connected():
        tasks = [
            asyncio.create_task(run_subscription("kafka-pending-tx", kafka_pending_native_tx_handler, ws_manager, kafka_producer, rpc_manager)),
            asyncio.create_task(run_subscription("kafka-pending-tx", kafka_pending_erc20_tx_handler, ws_manager, kafka_producer, rpc_manager)),
            asyncio.create_task(monitor_subscription_queue(ws_manager.w3))
        ]

        await asyncio.gather(*tasks)
    else:
        logging.error("❌ Connection failed. Check WSS URL.")

async def monitor_subscription_queue(w3):
    while True:
        try:
            queue = w3.provider._request_processor._handler_subscription_queue
            size = queue.qsize()
            logging.info(f"📊 Subscription Queue Size: {size}")
        except Exception as e:
            logging.error(f"❌ Error monitoring subscription queue: {e}")
        await asyncio.sleep(5)