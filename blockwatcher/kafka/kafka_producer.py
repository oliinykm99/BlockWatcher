import asyncio
from aiokafka import AIOKafkaProducer
from config import KAFKA_BOOTSTRAP_SERVERS

class KafkaProducer:
    def __init__(self, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            api_version="auto"
        )
        self._is_connected = False

    async def connect(self):
        if not self._is_connected:
            await self.producer.start()
            self._is_connected = True
            print("✅ Connected to Kafka producer.")

    async def close(self):
        if self._is_connected:
            await self.producer.stop()
            self._is_connected = False
            print("🛑 Kafka producer connection closed.")

    async def send(self, topic, value, key=None, headers=None):
        if not self._is_connected:
            raise ConnectionError("Kafka producer is not connected.")
        await self.producer.send_and_wait(
            topic,
            value=value,
            key=key,
            headers=headers
        )
