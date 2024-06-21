import json
import os
from kafka import KafkaProducer


class KafkaProducerClient:
    def __init__(self) -> None:
        self.producer = KafkaProducer(
            bootstrap_servers=[
                f"{os.getenv('KAFKA_BROKER_0_HOST')}:{os.getenv('KAFKA_BROKER_0_PORT')}"
            ],
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def produce_message(self, topic, message):
        self.producer.send(topic, message)
        self.producer.flush()
