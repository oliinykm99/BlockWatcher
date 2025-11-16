import asyncio
import logging
from blockwatcher.subscriptions import sub_manager
#from blockwatcher.telegram import telegram_bot_handler
from blockwatcher.connectors.kafka_producer import KafkaProducer
from blockwatcher.connectors.websocket_manager import ws_manager
from blockwatcher.connectors.http_manager import rpc_manager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    #await telegram_bot_handler.start()()
    kafka_producer = KafkaProducer()
    await kafka_producer.connect()
    await ws_manager.connect()
    try:
        await sub_manager(kafka_producer, ws_manager, rpc_manager)
    except KeyboardInterrupt:
        logging.info("\n🛑 Stopped by user.")
    except asyncio.CancelledError:
        logging.info("\n🛑 Task was cancelled.")
    except Exception as e:
        logging.info(f"🛑 An error occurred: {e}")
    finally:
        await kafka_producer.close()

if __name__ == "__main__":
    asyncio.run(main())