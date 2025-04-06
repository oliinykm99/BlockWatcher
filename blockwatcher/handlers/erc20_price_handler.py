from web3.exceptions import ContractLogicError
from blockwatcher.utils.utils import fetch_token_price
from config import ERC20_ABI, ERC20_TRANSFER_SIGNATURE, ERC20_TRANSFER_FROM_SIGNATURE 

async def erc20_price_handler(handler_context, db_manager):
    w3 = handler_context.async_w3
    tx_hash = '0x' + handler_context.result.hex()
    try:
        tx = await w3.eth.get_transaction(tx_hash)
        tx_input = "0x"+tx['input'].hex()

        if tx_input.startswith(ERC20_TRANSFER_SIGNATURE) or tx_input.startswith(ERC20_TRANSFER_FROM_SIGNATURE):
            contract = w3.eth.contract(address=tx['to'], abi=ERC20_ABI)
            method, _ = contract.decode_function_input(tx_input)

            if method.fn_name == "transfer":
                token_address, price_usd = await fetch_token_price(tx['to'])
                await db_manager.store_token_price(token_address, price_usd)
            
            elif method.fn_name == "transferFrom":
                token_address, price_usd = await fetch_token_price(tx['to'])
                await db_manager.store_token_price(token_address, price_usd)

    except ContractLogicError as e:
        print(f"⚠️ Contract error for transaction {tx_hash}: {e}")
    except Exception as e:
        print(f"⚠️ Error fetching transaction {tx_hash}: {e}")