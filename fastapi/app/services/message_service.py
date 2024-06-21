from app.kafka.producer import KafkaProducerClient
from app.models.message import Message


class MessageService:
    def __init__(self) -> None:
        self.producer_client = KafkaProducerClient()

    def send_message(self, message_data: dict):
        message = Message(**message_data)
        self.producer_client.produce_message(
            "chat-messages", message.model_dump(by_alias=True)
        )
