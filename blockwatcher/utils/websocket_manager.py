import asyncio
from web3 import AsyncWeb3
from config import WSS_URL

class WebSocketManager:
    def __init__(self, ws_url, max_retries):
        self.ws_url = ws_url
        self.w3 = None
        self.max_retries = max_retries

    async def connect(self):
        for attempt in range(1, self.max_retries+1):
            try: 
                print(f"🔄 Attempting WebSocket connection (Attempt {attempt}/{self.max_retries})...")
                self.w3 = await AsyncWeb3(AsyncWeb3.WebSocketProvider(self.ws_url))
                if await self.w3.is_connected():
                    print("✅ WebSocket connected successfully!")
                    return
            except Exception as e:
                print(f"🛑 WebSocket connection failed: {e}")
            await asyncio.sleep(2 ** attempt)
        print("❌ WebSocket connection failed after max retries.")

    async def is_connected(self):
        return self.w3 and await self.w3.is_connected()
    
ws_manager = WebSocketManager(WSS_URL, 5)
