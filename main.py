import asyncio
from blockwatcher.subscriptions import sub_manager
#from blockwatcher.telegram import telegram_bot_handler
from blockwatcher.kafka.kafka_producer import KafkaProducer
from blockwatcher.utils.websocket_manager import ws_manager
from blockwatcher.utils.http_manager import rpc_manager
from config import DB_URL

async def main():
    #await telegram_bot_handler.start()()
    kafka_producer = KafkaProducer()
    await kafka_producer.connect()
    await ws_manager.connect()
    try:
        await sub_manager(kafka_producer, ws_manager, rpc_manager)
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user.")
    except asyncio.CancelledError:
        print("\n🛑 Task was cancelled.")
    except Exception as e:
        print(f"🛑 An error occurred: {e}")
    finally:
        await kafka_producer.close()

if __name__ == "__main__":
    asyncio.run(main())