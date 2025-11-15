from config import ERC20_ABI, CHAINLINK_ETH_USD, CHAINLINK_ABI

async def fetch_token_metadata(w3, token_address, db_manager):
    token_metadata = await db_manager.get_token_metadata(token_address)
    if token_metadata:
        return token_metadata
    
    contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)
    try:
        name = await contract.functions.name().call()
        symbol = await contract.functions.symbol().call()
        decimals = await contract.functions.decimals().call()
        await db_manager.store_token_metadata(token_address, name, symbol, decimals)
        return token_address, name, symbol, decimals
    except Exception as e:
        print(f"⚠️ Error fetching metadata for {token_address}: {e}")
        return None
