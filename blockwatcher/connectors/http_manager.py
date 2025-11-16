import asyncio
from web3 import AsyncWeb3, AsyncHTTPProvider
from config import RPC_URL

class HTTPManager:
    def __init__(self, rpc_url, concurrency_limit=20):
        self.http_w3 = AsyncWeb3(AsyncHTTPProvider(rpc_url))
        self.concurrency_limiter = asyncio.Semaphore(concurrency_limit)

rpc_manager = HTTPManager(RPC_URL, 20)
