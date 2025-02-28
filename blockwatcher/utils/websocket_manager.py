from web3 import AsyncWeb3
from config import WSS_URL

class WebSocketManager:
    def __init__(self, ws_url):
        self.ws_url = ws_url
        self.w3 = None

    async def connect(self):
        if not self.w3:
            self.w3 = await AsyncWeb3(AsyncWeb3.WebSocketProvider(self.ws_url))

    async def is_connected(self):
        if self.w3:
            return await self.w3.is_connected()
        return False
    
ws_manager = WebSocketManager(WSS_URL)
