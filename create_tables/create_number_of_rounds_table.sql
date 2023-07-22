CREATE TABLE IF NOT EXISTS number_of_rounds(
    chat_id int,
    number_of_rounds int,
    UNIQUE(chat_id)
)