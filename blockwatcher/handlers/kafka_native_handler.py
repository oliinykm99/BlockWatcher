import json
import logging
from config import KAFKA_PENDING_TRANSACTIONS_TOPIC
from web3.exceptions import ContractLogicError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def kafka_pending_native_tx_handler(handler_context, kafka_producer, rpc_manager):
    #w3 = handler_context.async_w3
    tx_hash = '0x' + handler_context.result.hex()
    try:
        #tx = await w3.eth.get_transaction(tx_hash)
        async with rpc_manager.concurrency_limiter:
            tx = await rpc_manager.http_w3.eth.get_transaction(tx_hash)

        if tx['value']>0:
            print(f"💰 Native ETH Transfer Detected\n"
                  f"From: {tx['from']}\n"
                  f"To: {tx['to']}\n"
                  f"Value: {tx['value']}\n"
                  f"Gas: {tx['gas']}\n"
                  f"Gas Price: {tx['gasPrice']}\n"
                  f"Hash: {tx_hash}")

            value = json.dumps({'tx_hash': tx_hash,
                                'from': tx['from'],
                                'to': tx['to'],
                                'value': tx['value'],
                                'gas': tx['gas'],
                                'gasPrice': tx['gasPrice']})
            
            key = tx_hash

            headers = [('type', b'pending_native_transfer'),
                       ('source', b'publicNode')]

            await kafka_producer.send(topic=KAFKA_PENDING_TRANSACTIONS_TOPIC,
                                      value=value.encode('utf-8'),
                                      key=key.encode('utf-8'),
                                      headers=headers)
            print('-'*75)
            print('\n')
    except ContractLogicError as e:
        logging.critical(f"⚠️ Contract error for transaction {tx_hash}: {e}")
    except Exception as e:
        logging.error(f"⚠️ Error fetching transaction {tx_hash}: {e}")
