from web3.utils.subscriptions import PendingTxSubscription
from blockwatcher.handlers import pending_native_tx_handler, pending_erc20_tx_handler, erc20_handler, erc20_price_handler
from blockwatcher.utils import ws_manager

async def sub_manager(db_manager):
    """Sets up subscriptions for pending transactions."""
    await ws_manager.connect()

    if await ws_manager.is_connected():
        print("✅ Connected to Ethereum WebSocket!")
        w3 = ws_manager.w3

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
        
        erc20_token_price = PendingTxSubscription(
            label="erc20-tokens-price",
            full_transactions=True,
            handler=lambda ctx: erc20_price_handler(ctx, w3, db_manager))

        await w3.subscription_manager.subscribe([pending_native_tx, pending_erc20_tx, erc20_token, erc20_token_price])
        await w3.subscription_manager.handle_subscriptions()
    else:
        print("❌ Connection failed. Check WSS URL.")
