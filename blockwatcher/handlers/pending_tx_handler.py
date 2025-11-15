from web3.exceptions import ContractLogicError

async def pending_native_tx_handler(handler_context, w3, db_manager):
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

    except ContractLogicError as e:
        print(f"⚠️ Contract error for transaction {tx_hash}: {e}")
    except Exception as e:
        print(f"⚠️ Error fetching transaction {tx_hash}: {e}")
