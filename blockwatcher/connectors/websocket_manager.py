import asyncio
import logging
from web3 import AsyncWeb3
from config import WSS_URL

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WebSocketManager:
    def __init__(self, ws_url, max_retries):
        self.ws_url = ws_url
        self.w3 = None
        self.max_retries = max_retries

    async def connect(self):
        for attempt in range(1, self.max_retries+1):
            try: 
                logging.info(f"🔄 Attempting WebSocket connection (Attempt {attempt}/{self.max_retries})...")
                self.w3 = await AsyncWeb3(AsyncWeb3.WebSocketProvider(self.ws_url))
                if await self.w3.is_connected():
                    logging.info("✅ WebSocket connected successfully!")
                    return
            except Exception as e:
                logging.error(f"🛑 WebSocket connection failed: {e}")
            await asyncio.sleep(2 ** attempt)
        logging.critical("❌ WebSocket connection failed after max retries.")

    async def is_connected(self):
        return self.w3 and await self.w3.is_connected()
    
ws_manager = WebSocketManager(WSS_URL, 5)
