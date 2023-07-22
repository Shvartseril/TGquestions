CREATE TABLE IF NOT EXISTS questions(
    question_id int,
    question varchar(255),
    answer varchar(255),
    subject varchar(255),
    UNIQUE(question_id, question)
)
