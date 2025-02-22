from web3.utils.subscriptions import PendingTxSubscriptionContext
from web3.exceptions import ContractLogicError
from blockwatcher.utils.utils import fetch_token_metadata
from config import ERC20_ABI, ERC20_TRANSFER_SIGNATURE, ERC20_TRANSFER_FROM_SIGNATURE 

async def pending_tx_handler(handler_context, w3, db_manager):
    tx_hash = '0x' + handler_context.result.hex()
    try:
        tx = await w3.eth.get_transaction(tx_hash)
        tx_input = "0x"+tx['input'].hex()

        if tx['value']>0:
            print(f"💰 Native ETH Transfer Detected\n"
                  f"From: {tx['from']}\n"
                  f"To: {tx['to']}\n"
                  f"Value: {tx['value']}\n"
                  f"Gas: {tx['gas']}\n"
                  f"Gas Price: {tx['gasPrice']}\n"
                  f"Hash: {tx_hash}")
            await db_manager.store_pending_tx(tx_hash, "NATIVE", tx['from'], tx['to'], tx['value'], tx['gas'], tx['gasPrice'])
            print('-'*75)
            print('\n')

        elif tx_input.startswith(ERC20_TRANSFER_SIGNATURE) or tx_input.startswith(ERC20_TRANSFER_FROM_SIGNATURE):
            contract = w3.eth.contract(address=tx['to'], abi=ERC20_ABI)
            method, args = contract.decode_function_input(tx_input)

            if method.fn_name == "transfer":
                token_address, name, symbol, decimals = await fetch_token_metadata(w3, tx['to'])
                await db_manager.store_token_metadata(token_address, name, symbol, decimals)

                print(f"🦈 Whale Transfer Detected\n"
                      f"Token: {tx['to']}\n"
                      f"From: {tx['from']}\n"
                      f"To: {args['to']}\n"
                      f"Value: {args['value']}\n"
                      f"Gas: {tx['gas']}\n"
                      f"Gas Price: {tx['gasPrice']}\n"
                      f"Hash: {tx_hash}")
                await db_manager.store_pending_tx(tx_hash, tx['to'], tx['from'], args['to'], args['value'], tx['gas'], tx['gasPrice'])
                print('-'*75)
                print('\n')
            
            elif method.fn_name == "transferFrom":
                token_address, name, symbol, decimals = await fetch_token_metadata(w3, tx['to'])
                await db_manager.store_token_metadata(token_address, name, symbol, decimals)

                print(f"🦈 Whale Transfer Detected\n"
                      f"Token: {tx['to']}\n"
                      f"From: {args['from']}\n"
                      f"To: {args['to']}\n"
                      f"Value: {args['value']}\n"
                      f"Gas: {tx['gas']}\n"
                      f"Gas Price: {tx['gasPrice']}\n"
                      f"Hash: {tx_hash}")
                await db_manager.store_pending_tx(tx_hash, tx['to'], args['from'], args['to'], args['value'], tx['gas'], tx['gasPrice'])
                print('-'*75)
                print('\n')

    except ContractLogicError as e:
        print(f"⚠️ Contract error for transaction {tx_hash}: {e}")
    except Exception as e:
        print(f"⚠️ Error fetching transaction {tx_hash}: {e}")
