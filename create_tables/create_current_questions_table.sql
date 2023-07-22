CREATE TABLE IF NOT EXISTS current_questions (
    chat_id int,
    question_id int,
    UNIQUE(chat_id)
)