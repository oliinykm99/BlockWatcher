import json
import logging
from web3.exceptions import ContractLogicError
from blockwatcher.utils.utils import fetch_token_metadata
from blockwatcher.utils.decoder import decode_erc20_transfer, decode_erc20_transfer_from
from config import ERC20_TRANSFER_SIGNATURE, ERC20_TRANSFER_FROM_SIGNATURE, KAFKA_PENDING_TRANSACTIONS_ERC20_TOPIC 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def kafka_pending_erc20_tx_handler(handler_context, kafka_producer, rpc_manager):
    #w3 = handler_context.async_w3
    tx_hash = '0x' + handler_context.result.hex()
    try:
        async with rpc_manager.concurrency_limiter:
            tx = await rpc_manager.http_w3.eth.get_transaction(tx_hash)
       
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
        
        if amount_raw > 0:
            async with rpc_manager.concurrency_limiter:
                token_address, name, symbol, decimals = await fetch_token_metadata(rpc_manager.http_w3, tx['to'])

            value = json.dumps({'tx_hash': tx_hash,
                                'name': name,
                                'symbol': symbol,
                                'token_address': token_address,
                                'decimals': decimals,
                                'from': from_address if method_fn_name == 'transferFrom' else tx['from'],
                                'to': to_address,
                                'value': amount_raw,
                                'gas': tx['gas'],
                                'gasPrice': tx['gasPrice']})

            key = tx_hash

            headers = [('type', b'pending_erc20_transfer'),
                    ('source', b'publicNode')]
            
            await kafka_producer.send(topic=KAFKA_PENDING_TRANSACTIONS_ERC20_TOPIC,
                                    value=value.encode('utf-8'),
                                    key=key.encode('utf-8'),
                                    headers=headers)
    except ContractLogicError as e:
        logging.critical(f"⚠️ Contract error for transaction {tx_hash}: {e}")
    except Exception as e:
        logging.error(f"⚠️ Error fetching transaction {tx_hash}: {e}")