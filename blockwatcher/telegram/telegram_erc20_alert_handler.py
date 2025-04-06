from web3.exceptions import ContractLogicError
from blockwatcher.utils.utils import fetch_token_metadata, fetch_token_price
from config import ERC20_ABI, ERC20_TRANSFER_SIGNATURE, ERC20_TRANSFER_FROM_SIGNATURE 

counter = 0

async def telegram_erc20_alert_handler(handler_context, w3, telegram_bot_handler):
    global counter
    tx_hash = '0x' + handler_context.result.hex()
    try:
        tx = await w3.eth.get_transaction(tx_hash)
        tx_input = "0x"+tx['input'].hex()

        if tx_input.startswith(ERC20_TRANSFER_SIGNATURE) or tx_input.startswith(ERC20_TRANSFER_FROM_SIGNATURE):
            if tx['gas'] >= 34_500:
                contract = w3.eth.contract(address=tx['to'], abi=ERC20_ABI)
                method, args = contract.decode_function_input(tx_input)

                if method.fn_name in ["transfer", "transferFrom"]:
                    token_address, name, symbol, decimals = await fetch_token_metadata(w3, tx['to'])
                    amount_raw = args['value']
                    amount = amount_raw / (10**decimals)

                    
                    _, price_usd = await fetch_token_price(token_address)
                    amount_usd = amount * price_usd

                    counter +=1
                    print(counter, price_usd)

                    if amount_usd >= 10_000:
                        message = (
                                f"🚨 *Large Transfer Detected!*\n\n"
                                f"🔹 *Token*: {name} ({symbol})\n"
                                f"🔹 *From*: {tx['from'] if method.fn_name == 'transfer' else args['from']}\n"
                                f"🔹 *To*: {args['to']}\n"
                                f"🔹 *Amount*: {amount:,.2f} {symbol}\n"
                                f"💵 *Price*: ${price_usd}\n"
                                f"💵 *Value*: ${amount_usd:,.2f}\n"
                                f"🔗 [View on Etherscan](https://etherscan.io/tx/{tx_hash})")
                        await telegram_bot_handler.send_alert(message)

    except ContractLogicError as e:
        print(f"⚠️ Contract error for transaction {tx_hash}: {e}")
    except Exception as e:
        print(f"⚠️ Error fetching transaction {tx_hash}: {e}")