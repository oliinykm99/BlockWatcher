from web3 import AsyncWeb3
from web3.utils.subscriptions import PendingTxSubscription
from blockwatcher.handlers.pending_tx_handler import pending_native_tx_handler
from blockwatcher.handlers.erc20_pending_tx_handler import pending_erc20_tx_handler
from blockwatcher.handlers.erc20_handler import erc20_handler
from blockwatcher.database.db_manager import DatabaseManager
from config import WSS_URL


async def sub_manager(db_manager):
    """Sets up subscriptions for pending transactions."""
    w3 = await AsyncWeb3(AsyncWeb3.WebSocketProvider(WSS_URL))

    if await w3.is_connected():
        print("✅ Connected to Ethereum WebSocket!")

        pending_native_tx = PendingTxSubscription(
            label="pending-tx",
            full_transactions=True,
            handler=lambda ctx: pending_native_tx_handler(ctx, w3, db_manager))
        
        pending_erc20_tx = PendingTxSubscription(
            label="pending-erc20-tx",
            full_transactions=True,
            handler=lambda ctx: pending_erc20_tx_handler(ctx, w3, db_manager))
        
        erc20_token = PendingTxSubscription(
            label="erc20-tokens",
            full_transactions=True,
            handler=lambda ctx: erc20_handler(ctx, w3, db_manager))

        await w3.subscription_manager.subscribe([pending_native_tx, pending_erc20_tx, erc20_token])
        await w3.subscription_manager.handle_subscriptions()
    else:
        print("❌ Connection failed. Check WSS URL.")
