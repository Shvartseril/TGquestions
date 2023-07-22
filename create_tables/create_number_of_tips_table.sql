CREATE TABLE IF NOT EXISTS number_of_tips(
    chat_id int,
    number_of_tips int,
    UNIQUE(chat_id)
)