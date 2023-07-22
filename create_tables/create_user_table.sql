CREATE TABLE IF NOT EXISTS users (
    user_nickname varchar(255),
    chat_id int,
    UNIQUE(user_nickname)
)
