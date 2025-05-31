from fastapi import FastAPI
from contextlib import asynccontextmanager
from Core.kafka_producer import kafka_producer
from Core.kafka_consumer import kafka_consumer, handle_kafka_response

@asynccontextmanager
async def lifespan(app: FastAPI):
    await kafka_producer.start()
    await kafka_consumer.start(handle_kafka_response)
    yield
    await kafka_consumer.stop()
    await kafka_producer.stop()
app = FastAPI(lifespan=lifespan)


