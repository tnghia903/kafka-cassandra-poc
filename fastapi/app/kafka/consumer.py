import json
import os
from kafka import KafkaConsumer

from app.db.cassandra import CassandraClient
from app.models.message import Message


class KafkaConsumerClient:
    def __init__(self) -> None:
        self.consumer = KafkaConsumer(
            "chat-messages",
            bootstrap_servers=[
                f"{os.getenv('KAFKA_BROKER_0_HOST')}:{os.getenv('KAFKA_BROKER_0_PORT')}"
            ],
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )
        self.cassandra_client = CassandraClient()

    def consume_message(self):
        for message in self.consumer:
            msg_data = message.value
            msg = Message(**msg_data)
            self.cassandra_client.insert_message(msg)
