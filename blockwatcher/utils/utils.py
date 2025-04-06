import requests
from config import ERC20_ABI, ANKR_API

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
    
def fetch_token_price_cg(token_address, network="ethereum"):
    url = f"https://api.coingecko.com/api/v3/simple/token_price/{network}"
    params = {
        "contract_addresses": token_address,
        "vs_currencies": "usd"
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            usd_price = data.get(token_address.lower(), {}).get("usd")
            if usd_price is not None:
                return token_address, usd_price
        print(f"⚠️ Token not found or no USD price: {token_address}")
        return token_address, None
    except Exception as e:
        print(f"⚠️ Error fetching price for {token_address}: {e}")
        return token_address, None

def fetch_token_price_ankr(token_address, network="eth", api_key=ANKR_API):
    url = f"https://rpc.ankr.com/multichain/{api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "jsonrpc": "2.0",
        "method": "ankr_getTokenPrice",
        "params": {
            "blockchain": network,  
            "contractAddress": token_address
        },
        "id": 1
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            if 'result' in result:
                price_usd = result['result'].get('usdPrice')
                if price_usd is not None:
                    return token_address, float(price_usd)
        print(f"⚠️ Token not found or no USD price: {token_address}")
        return token_address, None
    except Exception as e:
        print(f"⚠️ Error fetching price for {token_address}: {e}")
        return token_address, None

def fetch_token_price(token_address):
    token, price = fetch_token_price_cg(token_address)
    if price is None:
        token, price = fetch_token_price_ankr(token_address)
    if price is None:
        print(f"⚠️ Failed to fetch price for {token_address} from both APIs.")
    
    return token, price  