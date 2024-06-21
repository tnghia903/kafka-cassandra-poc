import threading
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

from app.api import endpoints
from app.kafka.consumer import KafkaConsumerClient
from app.websockets.websocket_manager import websocket_endpoint

load_dotenv()

app = FastAPI()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="app/html"), name="static")

# Include API router
app.include_router(endpoints.router)


# Include WebSocket endpoint
app.add_api_websocket_route("/ws/{chat_id}", websocket_endpoint)


@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    # Start Kafka consumer in the background
    kafka_consumer = KafkaConsumerClient()
    kafka_consumer_thread = threading.Thread(target=kafka_consumer.consume_message)
    kafka_consumer_thread.start()


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")
