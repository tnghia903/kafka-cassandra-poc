import json
import threading
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

from app.api import endpoints
from app.kafka.consumer import KafkaConsumerClient
from app.websockets.websocket_manager import WebSocketManager

load_dotenv()

app = FastAPI()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="app/html"), name="static")

# Include API router
app.include_router(endpoints.router)


# Include WebSocket endpoint
websocket_manager = WebSocketManager()


async def websocket_endpoint(websocket: WebSocket, chat_id: str):
    await websocket_manager.connect(websocket, chat_id)
    try:
        while True:
            message = await websocket.receive_json()
            await websocket_manager.broadcast(chat_id, message)
    except WebSocketDisconnect as e:
        print(f"Runtime Error: {e}")
        websocket_manager.disconnect(websocket, chat_id)


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
