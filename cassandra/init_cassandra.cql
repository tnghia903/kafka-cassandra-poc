-- Create a keyspace
CREATE KEYSPACE IF NOT EXISTS chat WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': '1'};

USE chat;

CREATE TABLE IF NOT EXISTS messages (
    chat_id UUID,
    message_id UUID,
    sender_id UUID,
    content TEXT,
    timestamp BIGINT,
    PRIMARY KEY (chat_id, message_id)
);