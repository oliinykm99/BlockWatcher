from web3.exceptions import ContractLogicError
from blockwatcher.utils.utils import fetch_token_price

async def telegram_native_alert_handler(handler_context, telegram_bot_handler):
    async_w3 = handler_context.async_w3
    tx_hash = '0x' + handler_context.result.hex()
    try:
        tx = await async_w3.eth.get_transaction(tx_hash)
        if tx['value'] <= 5*(10**18) or tx['gas'] < 21_000:
            return        

        _, price_usd = fetch_token_price(token_address="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")
        amount_raw = tx['value']
        amount = amount_raw / (10**18)
        amount_usd = amount * price_usd
        
        message = (
                    f"🚨 *Large Transfer Detected!*\n\n"
                    f"🔹 *Token*: Ether (ETH)\n"
                    f"🔹 *From*: {tx['from']}\n"
                    f"🔹 *To*: {tx['to']}\n"
                    f"🔹 *Amount*: {amount:,.2f} ETH\n"
                    f"💵 *Price*: ${price_usd}\n" \
                    f"💵 *Value*: ${amount_usd:,.2f}\n"
                    f"🔗 [View on Etherscan](https://etherscan.io/tx/{tx_hash})")
        await telegram_bot_handler.send_alert(message)

    except ContractLogicError as e:
        print(f"⚠️ Contract error for transaction {tx_hash}: {e}")
    except Exception as e:
        print(f"⚠️ Error fetching transaction {tx_hash}: {e}")
