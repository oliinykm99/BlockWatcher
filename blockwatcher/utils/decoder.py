from eth_abi import decode
from eth_utils import to_bytes
from config import ERC20_TRANSFER_SIGNATURE, ERC20_TRANSFER_FROM_SIGNATURE

def decode_erc20_transfer(tx_input):
    if tx_input[:10] != ERC20_TRANSFER_SIGNATURE:
        return None
    to_address, amount = decode(['address', 'uint256'], to_bytes(hexstr=tx_input[10:]))
    return to_address, amount

def decode_erc20_transfer_from(tx_input):
    if tx_input[:10] != ERC20_TRANSFER_FROM_SIGNATURE:
        return None
    data = to_bytes(hexstr=tx_input[10:])
    from_address = decode(['address'], data[:32])[0]
    to_address = decode(['address'], data[32:64])[0]
    amount = decode(['uint256'], data[64:])[0]
    
    return from_address, to_address, amount