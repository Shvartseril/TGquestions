from questions import create_all_questions
import telebot
from telebot import types
import time
import sys
import random

import sqlite3


TOKEN: str = "6042304934:AAFxt1sXWNAwPoIgzDcscr_pAZIlr7LTAAg"
connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = connection.cursor()


def open_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()


def select(where_from, where_what, is_what, cursor=cursor):
    sql_command = f'SELECT * FROM {where_from} WHERE {where_what} = {is_what}'
    cursor.execute(sql_command)
    return cursor.fetchmany()[0]


def delete(where_from, where_what, is_what):
    sql_command = f'DELETE FROM {where_from} WHERE {where_what} = {is_what}'
    cursor.execute(sql_command)
    connection.commit()


def update(where_from, set_what, is_what, where_what, what, cursor=cursor):
    sql_command = f'UPDATE {where_from} SET {set_what} = {is_what} WHERE {where_what} = {what}'
    cursor.execute(sql_command)
    connection.commit()


def create_table(file_name: str):
    cursor.execute(open_file(file_name))
    connection.commit()


class Bot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(TOKEN)

    def start_message(self, message):
        self.bot.reply_to(message, f"Привет, {message.from_user.first_name} {message.from_user.last_name}! Я еще не "
                                   f"придумал название, "
                                   " \nДавай начинать!")

        time.sleep(1)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_history = types.KeyboardButton("История 📚")
        markup.add(button_history)
        self.bot.send_message(message.chat.id, 'Выбери любую тему вопросов', reply_markup=markup)


class Question:
    def __init__(self, bot):

        self.get_random_question_sql = open_file('commands_for_tables/get_random_question.sql')
        self.add_into_number_of_rounds_sql = open_file('commands_for_tables/add_into_number_of_rounds_table.sql')
        self.add_into_solved_sql = open_file('commands_for_tables/add_into_solved_table.sql')
        self.add_into_current_questions_sql = open_file('commands_for_tables/add_into_current_questions_table.sql')

    def check_is_right_answer(self, message):
        # потому что этот вонючий sqlite3 не хочет с одним курсором работать в нескольких потоках,
        # знаете ли, совсем обнаглел уже, 3000 лет пытался понять, что этому козлу не нравится, наконец понял
        cursor = connection.cursor()

        find_current_question = select('current_questions', 'chat_id', message.chat.id, cursor)

        all_question = select('questions', 'question_id', find_current_question[1], cursor)

        if message.text == all_question[2]:
            cursor.execute(self.add_into_solved_sql, [message.chat.id, all_question[0]])

            connection.commit()

            my_bot.bot.send_message(message.chat.id, "Правильно")
            update('number_of_tips', 'number_of_tips', 0, 'chat_id', message.chat.id, cursor)
            update('right_answer', 'is_right_answer', 1, 'chat_id', message.chat.id, cursor)
            return
        my_bot.bot.send_message(message.chat.id, "Неправильно")

    def number_of_rounds(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        ten = types.KeyboardButton("🔟 раундов")
        markup.add(ten)

        my_bot.bot.send_message(message.chat.id, "Выберите Количество Раундов", reply_markup=markup)

    def make_new_question(self, message, first_question=False):
        if not first_question:
            delete('current_questions', 'chat_id', message.chat.id)

        get_new_question = self.get_random_question_sql
        cursor.execute(get_new_question)
        new_question = cursor.fetchmany()[0]

        cursor.execute(self.add_into_current_questions_sql, [message.chat.id, new_question[0]])
        connection.commit()

        if first_question:
            my_bot.bot.send_message(message.chat.id, new_question[1], reply_markup=types.ReplyKeyboardRemove())
        else:
            my_bot.bot.send_message(message.chat.id, new_question[1])

    def __make_tip(self, message):
        current_question = select('current_questions', 'chat_id', message.chat.id)

        all_question = select('questions', 'question_id', current_question[1])

        number_of_tips = select('number_of_tips', 'chat_id', message.chat.id)[1]
        answer = all_question[2]

        tip = ''
        for i in range(len(answer)):
            if answer[i] == ' ':
                tip += '  '
            else:
                tip += '_ '

        if number_of_tips == 0:
            my_bot.bot.send_message(message.chat.id, f"Подсказка: {tip}")
        elif number_of_tips == 1:
            my_bot.bot.send_message(message.chat.id, f"Подсказка2: {tip}")
        elif number_of_tips == 2:
            my_bot.bot.send_message(message.chat.id, f"Подсказка3: {tip}")

    def start_making_tips(self, message):
        time_for_tips = time.time()

        while True:
            if time.time() - time_for_tips > 5:
                number_of_tips = select('number_of_tips', 'chat_id', message.chat.id)[1]

                time_for_tips = time.time()

                if number_of_tips == 3:

                    current_question = select('current_questions', 'chat_id', message.chat.id)

                    all_question = select('questions', 'question_id', current_question[1])

                    my_bot.bot.send_message(message.chat.id, 'Ответ')
                    my_bot.bot.send_message(message.chat.id, all_question[2])

                    cursor.execute(self.add_into_solved_sql, [message.chat.id, all_question[0]])

                    connection.commit()

                    update('number_of_tips', 'number_of_tips', 0, 'chat_id', message.chat.id)
                    time.sleep(1)

                    update('number_of_tips', 'number_of_tips', 0, 'chat_id', message.chat.id)
                    return

                self.__make_tip(message)
                number_of_tips = select('number_of_tips', 'chat_id', message.chat.id)[1]

                update('number_of_tips', 'number_of_tips', number_of_tips + 1, 'chat_id', message.chat.id)

            right_answer = select('right_answer', 'chat_id', message.chat.id)

            if right_answer[1] == 1:
                update('right_answer', 'is_right_answer', 0, 'chat_id', message.chat.id, cursor)
                return


my_bot = Bot(TOKEN)
question = Question(my_bot)


# Добавить возможность присутсвия в группе
# сделать лучше обработчик ответов
# подсказки сделать лучше
@my_bot.bot.message_handler(commands=['start'])
def handler_start(message):
    if message.text == '/start':
        create_table("create_tables/create_number_of_rounds_table.sql")

        delete('number_of_rounds', 'chat_id', message.chat.id)

        create_table('create_tables/create_user_table.sql')

        create_user = open_file('commands_for_tables/add_into_user_table.sql')
        cursor.execute(create_user, [message.from_user.username, message.chat.id])

        create_table('create_tables/create_question_table.sql')

        create_table('create_tables/create_solved_table.sql')
        delete('solved', 'chat_id', message.chat.id)

        create_table('create_tables/create_current_questions_table.sql')
        delete('current_questions', 'chat_id', message.chat.id)

        create_table('create_tables/create_number_of_tips_table.sql')

        create_number_of_tips = open_file('commands_for_tables/add_into_number_of_tips_table.sql')
        cursor.execute(create_number_of_tips, [message.chat.id, 0])

        create_table('create_tables/create_right_answer_table.sql')
        create_right_answer = open_file('commands_for_tables/add_into_right_answer_table.sql')
        cursor.execute(create_right_answer, [message.chat.id, 0])
        update('right_answer', 'is_right_answer', 0, 'chat_id', message.chat.id)

        update('number_of_tips', 'number_of_tips', 0, 'chat_id', message.chat.id)

        create_all_questions(cursor)

        connection.commit()

        my_bot.start_message(message)


@my_bot.bot.message_handler(commands=['stop'])
def handler_stop(message):
    if message.text == '/stop':
        my_bot.bot.send_message(message.chat.id, 'Я вас понял, я обиделся, не ждите меня тут больше')
        my_bot.bot.stop_polling()
        connection.close()
        sys.exit()


@my_bot.bot.message_handler(content_types=['text'])
def run(message):

    if message.text == "🔟 раундов":
        cursor.execute(question.add_into_number_of_rounds_sql, [message.chat.id, 10])
        connection.commit()

        question.make_new_question(message, True)
        question.start_making_tips(message)

        for i in range(9):
            question.make_new_question(message)
            question.start_making_tips(message)

    elif message.text == "История 📚":
        question.number_of_rounds(message)

    else:
        question.check_is_right_answer(message)


def main():
    my_bot.bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
