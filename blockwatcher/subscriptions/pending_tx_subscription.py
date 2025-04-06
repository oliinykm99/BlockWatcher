import asyncio
from web3.utils.subscriptions import PendingTxSubscription
from blockwatcher.handlers import pending_native_tx_handler, pending_erc20_tx_handler, erc20_handler, erc20_price_handler
from blockwatcher.utils import ws_manager

async def run_subscription(label, handler, db_manager):
    """Run a single subscription."""
    w3 = ws_manager.w3
    subscription = PendingTxSubscription(
        label=label,
        full_transactions=True,
        handler=lambda ctx: handler(ctx, db_manager)
    )
    await w3.subscription_manager.subscribe([subscription])
    await w3.subscription_manager.handle_subscriptions()

async def sub_manager(db_manager):
    """Starts independent workers for each subscription."""
    await ws_manager.connect()

    if await ws_manager.is_connected():
        print("✅ Connected to Ethereum WebSocket!")

        tasks = [
            asyncio.create_task(run_subscription("pending-tx", pending_native_tx_handler, db_manager)),
            asyncio.create_task(run_subscription("pending-erc20-tx", pending_erc20_tx_handler, db_manager)),
            asyncio.create_task(run_subscription("erc20-tokens", erc20_handler, db_manager)),
            #asyncio.create_task(run_subscription("erc20-tokens-price", erc20_price_handler, db_manager)),
        ]

        await asyncio.gather(*tasks)
    else:
        print("❌ Connection failed. Check WSS URL.")