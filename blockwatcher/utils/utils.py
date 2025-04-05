import aiohttp
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
    
async def fetch_token_price(token_address, network="ethereum"):
    url = f"https://api.coingecko.com/api/v3/simple/token_price/{network}"
    params = {
        "contract_addresses": token_address,
        "vs_currencies": "usd"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    usd_price = data.get(token_address.lower(), {}).get("usd")
                    if usd_price is not None:
                        return token_address, usd_price
                print(f"⚠️ Token not found or no USD price: {token_address}")
                return token_address, None
    except Exception as e:
        print(f"⚠️ Error fetching price for {token_address}: {e}")
        return token_address, None            