from web3.exceptions import ContractLogicError
from config import ERC20_TRANSFER_SIGNATURE, ERC20_TRANSFER_FROM_SIGNATURE
from blockwatcher.utils.decoder import decode_erc20_transfer, decode_erc20_transfer_from 

async def pending_erc20_tx_handler(handler_context, db_manager):
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

        if method_fn_name == "transfer":
            print(f"🦈 Whale Transfer Detected\n"
                    f"Token: {tx['to']}\n"
                    f"From: {tx['from']}\n"
                    f"To: {to_address}\n"
                    f"Value: {amount_raw}\n"
                    f"Gas: {tx['gas']}\n"
                    f"Gas Price: {tx['gasPrice']}\n"
                    f"Hash: {tx_hash}")
            await db_manager.store_pending_tx(tx_hash, tx['to'], tx['from'], to_address, amount_raw, tx['gas'], tx['gasPrice'])
            print('-'*75)
            print('\n')
        
        elif method_fn_name == "transferFrom":
            print(f"🦈 Whale Transfer Detected\n"
                    f"Token: {tx['to']}\n"
                    f"From: {from_address}\n"
                    f"To: {to_address}\n"
                    f"Value: {amount_raw}\n"
                    f"Gas: {tx['gas']}\n"
                    f"Gas Price: {tx['gasPrice']}\n"
                    f"Hash: {tx_hash}")
            await db_manager.store_pending_tx(tx_hash, tx['to'], from_address, to_address, amount_raw, tx['gas'], tx['gasPrice'])
            print('-'*75)
            print('\n')

    except ContractLogicError as e:
        print(f"⚠️ Contract error for transaction {tx_hash}: {e}")
    except Exception as e:
        print(f"⚠️ Error fetching transaction {tx_hash}: {e}")
