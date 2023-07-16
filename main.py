import telebot
from telebot import types
import time
import random
from enum import Enum

TOKEN: str = "6042304934:AAFxt1sXWNAwPoIgzDcscr_pAZIlr7LTAAg"

history_questions = {'В каком году Колумб открыл америку?': '1492', 'В каком году отменили крепостное право?': '1861',
                     'Кто был первый царь Рима?': 'Ромул'}


class Subject(Enum):
    NOTHING = 0
    HISTORY = 1


class Bot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(TOKEN)
        self.subject = Subject.NOTHING

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
        self.subject = Subject.NOTHING
        self.questions = list(history_questions.keys())
        self.current_question = random.randint(0, len(self.questions) - 1)
        self.start_time = None
        self.right_answer = False
        self.number_tips = 0

    def check_is_right_answer(self, message):
        if self.subject == Subject.HISTORY:
            answer = history_questions[self.questions[self.current_question]]
            if message.text == answer:
                my_bot.bot.send_message(message.chat.id, "Правильно")
                self.__update_question__()
                time.sleep(1)
                self.make_new_question(message)
                return True
            my_bot.bot.send_message(message.chat.id, "Неправильно")
            return False

    def __update_question__(self):
        del history_questions[self.questions[self.current_question]]
        self.questions.pop(self.current_question)
        self.current_question = random.randint(0, len(self.questions) - 1)
        self.right_answer = False
        self.start_time = time.time()

    def make_new_question(self, message):
        if self.subject == Subject.HISTORY:
            my_bot.bot.send_message(message.chat.id, self.questions[self.current_question])
            self.start_time = time.time()

        self.start_making_tips(message)

    def __make_tip__(self, message):

        answer = history_questions[self.questions[self.current_question]]
        if self.number_tips == 0:
            my_bot.bot.send_message(message.chat.id, f"Подсказка: {'_ ' * len(answer)}")
        elif self.number_tips == 1:
            my_bot.bot.send_message(message.chat.id, f"Подсказка2: {'_ ' * len(answer)}")
        elif self.number_tips == 2:
            my_bot.bot.send_message(message.chat.id, f"Подсказка3: {'_ ' * len(answer)}")

    def start_making_tips(self, message):
        if self.subject == Subject.HISTORY:
            while True:
                if time.time() - self.start_time > 5:
                    if self.number_tips == 3:
                        my_bot.bot.send_message(message.chat.id, 'Ответ')

                        self.__update_question__()
                        time.sleep(1)
                        self.number_tips = 0
                        self.make_new_question(message)
                        break

                    self.__make_tip__(message)
                    self.number_tips += 1
                    self.start_time = time.time()

                if self.right_answer:
                    self.right_answer = False
                    self.number_tips = 0
                    break


my_bot = Bot(TOKEN)
question = Question(my_bot)


@my_bot.bot.message_handler(commands=['start', 'stop'])
def handler(message):
    if message.text == '/start' and my_bot.subject == Subject.NOTHING:
        my_bot.start_message(message)
    elif message.text == '/stop':
        my_bot.bot.send_message(message.chat.id, 'Я вас понял, я обиделся, не ждите меня тут больше')
        my_bot.bot.stop_polling()


@my_bot.bot.message_handler(content_types=['text'])
def run(message):
    if message.text == "История 📚" and question.subject == Subject.NOTHING:
        question.subject = Subject.HISTORY
        question.make_new_question(message)

    else:
        question.check_is_right_answer(message)


def main():
    my_bot.bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
