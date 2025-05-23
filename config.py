import os
from dotenv import load_dotenv

load_dotenv()

WSS_URL = os.getenv('WSS_URL')
DB_URL = os.getenv('DB_URL')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')


# Constants
# ERC20 ABI
ERC20_ABI = [
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
    {
        "name": "decimals",
        "type": "function",
        "inputs": [],
        "outputs": [{"name": "", "type": "uint8"}],
    },
    {
        "name": "name",
        "type": "function",
        "inputs": [],
        "outputs": [{"name": "", "type": "string"}],
    },
    {
        "name": "symbol",
        "type": "function",
        "inputs": [],
        "outputs": [{"name": "", "type": "string"}],
    }
]

ERC20_TRANSFER_SIGNATURE = "0xa9059cbb"  # transfer(address,uint256)
ERC20_TRANSFER_FROM_SIGNATURE = "0x23b872dd"  # transferFrom(address,address,uint256)