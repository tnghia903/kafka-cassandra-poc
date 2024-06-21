import os
import uuid
from app.models.message import Message
from cassandra.cluster import Cluster


class CassandraClient:
    def __init__(self) -> None:
        self.cluster = Cluster([os.getenv("CASSANDRA_HOST") or "127.0.0.1"])
        self.session = self.cluster.connect()

    def insert_message(self, message: Message):
        self.session.execute(
            """
            INSERT INTO chat.messages (chat_id, message_id, content, sender_id, timestamp) VALUES (%s, %s, %s, %s, %s)
            """,
            (
                uuid.UUID(message.chat_id),
                uuid.UUID(message.message_id),
                message.content,
                uuid.UUID(message.sender_id),
                message.timestamp,
            ),
        )
