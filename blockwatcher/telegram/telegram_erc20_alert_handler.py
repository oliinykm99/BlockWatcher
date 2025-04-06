import asyncio
from web3.exceptions import ContractLogicError
from blockwatcher.utils.utils import fetch_token_metadata
from blockwatcher.utils.decoder import decode_erc20_transfer, decode_erc20_transfer_from
from config import ERC20_ABI, ERC20_TRANSFER_SIGNATURE, ERC20_TRANSFER_FROM_SIGNATURE 

async def telegram_erc20_alert_handler(handler_context, telegram_bot_handler):
    w3 = handler_context.async_w3
    tx_hash = '0x' + handler_context.result.hex()
    try:
        tx = await w3.eth.get_transaction(tx_hash)
        tx_input = "0x"+tx['input'].hex()

        if tx_input.startswith(ERC20_TRANSFER_SIGNATURE):
            decoded = decode_erc20_transfer(tx_input)
            if decoded:
                to_address, amount_raw = decoded
                method_fn_name = "transfer"
        elif tx_input.startswith(ERC20_TRANSFER_FROM_SIGNATURE):
            decoded = decode_erc20_transfer_from(tx_input)
            if decoded:
                from_address, to_address, amount_raw = decoded
                method_fn_name = "transferFrom"
        else:
            return
        
        if tx['gas'] <= 40_000:
            return
        
        token_address, name, symbol, decimals = await fetch_token_metadata(w3, tx['to'])
        amount = amount_raw / (10**decimals)

        if amount >= 10_000:
            message = (
                    f"🚨 *Large Transfer Detected!*\n\n"
                    f"🔹 *Token*: {name} ({symbol})\n"
                    f"🔹 *From*: {from_address if method_fn_name == 'transferFrom' else tx['from']}\n"
                    f"🔹 *To*: {to_address}\n"
                    f"🔹 *Amount*: {amount:,.2f} {symbol}\n"
                    #f"💵 *Price*: ${price_usd:,.2f}\n"
                    #f"💵 *Value*: ${amount_usd:,.2f}\n"
                    f"🔗 [View on Etherscan](https://etherscan.io/tx/{tx_hash})")
            await telegram_bot_handler.send_alert(message)

    except ContractLogicError as e:
        print(f"⚠️ Contract error for transaction {tx_hash}: {e}")
    except Exception as e:
        print(f"⚠️ Error fetching transaction {tx_hash}: {e}")