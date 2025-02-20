from web3.utils.subscriptions import PendingTxSubscriptionContext
from web3.exceptions import ContractLogicError

# ERC20 ABI
erc20_abi = [
    {
        "name": "transfer",
        "type": "function",
        "inputs": [
            {"name": "to", "type": "address"},
            {"name": "value", "type": "uint256"}
        ],
        "outputs": [{"name": "", "type": "bool"}],
    },
    {
        "name": "transferFrom",
        "type": "function",
        "inputs": [
            {"name": "from", "type": "address"},
            {"name": "to", "type": "address"},
            {"name": "value", "type": "uint256"}
        ],
        "outputs": [{"name": "", "type": "bool"}],
    },
]

ERC20_TRANSFER_SIGNATURE = "0xa9059cbb"  # transfer(address,uint256)
ERC20_TRANSFER_FROM_SIGNATURE = "0x23b872dd"  # transferFrom(address,address,uint256)

async def pending_tx_handler(handler_context: PendingTxSubscriptionContext, w3):
    """Handles pending transaction events."""
    tx_hash = '0x' + handler_context.result.hex()
    try:
        tx = await w3.eth.get_transaction(tx_hash)
        tx_input = "0x"+tx['input'].hex()

        if tx['value']>0:
            print("💰 Native ETH Transfer Detected")
            print(f"From: {tx['from']}")
            print(f"To: {tx['to']}")
            print(f"Value: {tx['value']}")
            print(f"Gas: {tx['gas']}")
            print(f"Gas Price: {tx['gasPrice']}")
            print(f"Hash: {tx_hash}")
            print('-'*50)
            print('\n')


        elif tx_input.startswith(ERC20_TRANSFER_SIGNATURE) or tx_input.startswith(ERC20_TRANSFER_FROM_SIGNATURE):
            contract = w3.eth.contract(address=tx['to'], abi=erc20_abi)
            method, args = contract.decode_function_input(tx_input)

            if method.fn_name == "transfer":
                token = tx['to']
                from_address = tx['from']
                to_address = args['to']
                value = args['value']
                gas = tx['gas']
                gasPrice = tx['gasPrice']
                print(f"🦈 Whale Transfer Detected")
                print(f'Token: {token}')
                print(f"From: {from_address}")
                print(f"To: {to_address}")
                print(f"Value: {value}")
                print(f"Gas: {gas}")
                print(f"Gas Price: {gasPrice}")
                print(f"Hash: {tx_hash}")
                print('-'*50)
                print('\n')
            
            elif method.fn_name == "transferFrom":
                token = tx['to']
                from_address = args['from']
                to_address = args['to']
                value = args['value']
                gas = tx['gas']
                gasPrice = tx['gasPrice']
                print("🦈 Whale TransferFrom Detected")
                print(f'Token: {token}')
                print(f"From: {from_address}")
                print(f"To: {to_address}")
                print(f"Value: {value}")
                print(f"Gas: {gas}")
                print(f"Gas Price: {gasPrice}")
                print(f"Hash: {tx_hash}")
                print('-'*50)
                print('\n')

    except ContractLogicError as e:
        print(f"⚠️ Contract error for transaction {tx_hash}: {e}")
    except Exception as e:
        print(f"⚠️ Error fetching transaction {tx_hash}: {e}")
