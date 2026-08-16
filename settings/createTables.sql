CREATE TABLE IF NOT EXISTS messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_ip varchar(15),
    message TEXT NOT NULL,
    room_key varchar(15),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_messages_room_key ON messages(room_key);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);
