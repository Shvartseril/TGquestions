CREATE TABLE IF NOT EXISTS right_answer(
    chat_id int,
    is_right_answer int,
    UNIQUE(chat_id)
)