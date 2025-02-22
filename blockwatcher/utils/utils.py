from web3 import AsyncWeb3
from config import ERC20_ABI

async def fetch_token_metadata(w3, token_address):
    contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)
    try:
        name = await contract.functions.name().call()
        symbol = await contract.functions.symbol().call()
        decimals = await contract.functions.decimals().call()

        return token_address, name, symbol, decimals
    except Exception as e:
        print(f"⚠️ Error fetching metadata for {token_address}: {e}")
        return None