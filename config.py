import os
from dotenv import load_dotenv

load_dotenv()

WSS_URL = os.getenv('WSS_URL')
RPC_URL = os.getenv('RPC_URL')
DB_URL = os.getenv('DB_URL')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')


# Kafka
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_PENDING_TRANSACTIONS_TOPIC = 'raw-pending-transactions'
KAFKA_PENDING_TRANSACTIONS_ERC20_TOPIC = 'raw-erc20-pending-transactions'
KAFKA_ETH_PRICE_TOPIC = 'eth-price'

# Chainlink Oracle
CHAINLINK_ETH_USD = "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"

# Constants
# ERC20 ABI
ERC20_ABI = [
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

CHAINLINK_ABI = [
    {
        "name": "latestRoundData",
        "type": "function",
        "inputs": [],
        "outputs": [
            { "name": "roundId", "type": "uint80" },
            { "name": "answer", "type": "int256" },
            { "name": "startedAt", "type": "uint256" },
            { "name": "updatedAt", "type": "uint256" },
            { "name": "answeredInRound", "type": "uint80" }],   
    },
    {
        "name": "decimals",
        "type": "function",
        "inputs": [],
        "outputs": [{ "name": "", "type": "uint8" }],
    }
]

ERC20_TRANSFER_SIGNATURE = "0xa9059cbb"  # transfer(address,uint256)
ERC20_TRANSFER_FROM_SIGNATURE = "0x23b872dd"  # transferFrom(address,address,uint256)