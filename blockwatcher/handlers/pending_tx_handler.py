from web3.utils.subscriptions import PendingTxSubscriptionContext
from web3.exceptions import ContractLogicError
from config import ERC20_ABI, ERC20_TRANSFER_SIGNATURE, ERC20_TRANSFER_FROM_SIGNATURE 

async def pending_tx_handler(handler_context: PendingTxSubscriptionContext, w3, db_manager):
    tx_hash = '0x' + handler_context.result.hex()
    try:
        tx = await w3.eth.get_transaction(tx_hash)
        tx_input = "0x"+tx['input'].hex()

        if tx['value']>0:
            token = "NATIVE"
            from_address = tx['from']
            to_address = tx['to']
            value = tx['value']
            gas = tx['gas']
            gas_price = tx['gasPrice']
            print(f"💰 Native ETH Transfer Detected\n"
                  f"From: {from_address}\n"
                  f"To: {to_address}\n"
                  f"Value: {value}\n"
                  f"Gas: {gas}\n"
                  f"Gas Price: {gas_price}\n"
                  f"Hash: {tx_hash}")
            await db_manager.store_pending_tx(tx_hash, token, from_address, to_address, value, gas, gas_price)
            print('-'*75)
            print('\n')

        elif tx_input.startswith(ERC20_TRANSFER_SIGNATURE) or tx_input.startswith(ERC20_TRANSFER_FROM_SIGNATURE):
            contract = w3.eth.contract(address=tx['to'], abi=ERC20_ABI)
            method, args = contract.decode_function_input(tx_input)

            if method.fn_name == "transfer":
                token = tx['to']
                from_address = tx['from']
                to_address = args['to']
                value = args['value']
                gas = tx['gas']
                gas_price = tx['gasPrice']
                print(f"🦈 Whale Transfer Detected\n"
                      f"Token: {token}\n"
                      f"From: {from_address}\n"
                      f"To: {to_address}\n"
                      f"Value: {value}\n"
                      f"Gas: {gas}\n"
                      f"Gas Price: {gas_price}\n"
                      f"Hash: {tx_hash}")
                await db_manager.store_pending_tx(tx_hash, token, from_address, to_address, value, gas, gas_price)
                print('-'*75)
                print('\n')
            
            elif method.fn_name == "transferFrom":
                token = tx['to']
                from_address = args['from']
                to_address = args['to']
                value = args['value']
                gas = tx['gas']
                gas_price = tx['gasPrice']
                print(f"🦈 Whale Transfer Detected\n"
                      f"Token: {token}\n"
                      f"From: {from_address}\n"
                      f"To: {to_address}\n"
                      f"Value: {value}\n"
                      f"Gas: {gas}\n"
                      f"Gas Price: {gas_price}\n"
                      f"Hash: {tx_hash}")
                await db_manager.store_pending_tx(tx_hash, token, from_address, to_address, value, gas, gas_price)
                print('-'*75)
                print('\n')

    except ContractLogicError as e:
        print(f"⚠️ Contract error for transaction {tx_hash}: {e}")
    except Exception as e:
        print(f"⚠️ Error fetching transaction {tx_hash}: {e}")
