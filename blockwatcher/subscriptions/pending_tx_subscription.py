from web3 import AsyncWeb3
from web3.utils.subscriptions import PendingTxSubscription
from blockwatcher.handlers.pending_tx_handler import pending_tx_handler
from blockwatcher.database.db_manager import DatabaseManager
from config import WSS_URL


async def sub_manager(db_manager):
    """Sets up subscriptions for pending transactions."""
    w3 = await AsyncWeb3(AsyncWeb3.WebSocketProvider(WSS_URL))

    if await w3.is_connected():
        print("✅ Connected to Ethereum WebSocket!")

        pending_tx = PendingTxSubscription(
            label="pending-tx-mainnet",
            full_transactions=True,
            handler=lambda ctx: pending_tx_handler(ctx, w3, db_manager))

        await w3.subscription_manager.subscribe([pending_tx])
        await w3.subscription_manager.handle_subscriptions()
    else:
        print("❌ Connection failed. Check WSS URL.")
