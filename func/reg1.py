import telebot
import pymysql
import time
from constants import incorrect_input_text, already_registered_text
bot = telebot.TeleBot("2018040395:AAHBdge6sSyCvSFM9mmzn1y4wrmKXbDhXmA")

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="0914kd",
    database="botDB"
)


def checkName(name):
    if len(name.split(' ')) == 3 and len(name.split(" ")[0]) > 1 and len(name.split(" ")[1]) > 1 and len(name.split(" ")[2]) > 1:
        return True
    return False


def checkDate(date):
    data = date.split(".")
    if len(data) != 3:
        return False
    if data[0].isdigit() and data[1].isdigit() and data[2].isdigit() and int(data[0]) in range(1, 32) and data[1] in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"] and \
            int(data[2]) in range(2004, 2019):
        return True


@bot.message_handler(commands=['start'])
def print_start(message):
    tID = message.chat.id
    with connection.cursor() as cursor:
        cursor.execute("select kid_firstname, kid_lastname from users where tID = \"" + str(tID) + "\"")
        data = cursor.fetchall()
    if not data:
        with connection.cursor() as cursor:
            cursor.execute("insert into users (tID) VALUES (\"" + str(tID) + "\")")
            connection.commit()
        bot.send_message(tID, "Привет! Добро пожаловать в ГосУслуги Кидс!")
        bot.send_message(
            tID, "Здесь ты сможешь найти кружок или спортивную секцию по своим предпочтениям")
        time.sleep(3)
        bot.send_message(
            tID, "Для начала использования необходимо зарегистрироваться")
        msg = bot.send_message(
            tID, "Напиши свою фамилию, имя и отчество через пробел")
        bot.register_next_step_handler(msg, input_name)
    else:
        print(data)
        bot.send_message(tID, str(data[0][1]) + ", ты уже зарегистрирован(а) в ГосУслугах Кидс")


def input_name(message):
    tID = message.chat.id
    data = message.text
    if not checkName(data):
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, input_name)
    else:
        with connection.cursor() as cursor:
            cursor.execute("update users set kid_firstname = \"" +
                           data.split(" ")[0] + "\" where tID = \"" + str(tID) + "\"")
            cursor.execute("update users set kid_lastname = \"" +
                           data.split(" ")[1] + "\" where tID = \"" + str(tID) + "\"")
            cursor.execute("update users set kid_patronymic = \"" +
                           data.split(" ")[2] + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()

        bot.send_message(
            tID, "Приятно познакомиться, " + data.split(" ")[1])
        msg = bot.send_message(
            tID, "Отправь мне свою дату рождения в формате ДД.ММ.ГГГГ")
        bot.register_next_step_handler(msg, input_date_birth)


def input_date_birth(message):
    tID = message.chat.id
    data = message.text
    if checkDate(data):
        with connection.cursor() as cursor:
            cursor.execute("update users set birth_date = \"" +
                           data + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
        bot.send_message(tID, "Записал дату рождения")
        msg = bot.send_message(
            tID, "Если у тебя есть сертификат ПФДО, отправь мне его номер. Если нет, отправь 0")
        bot.register_next_step_handler(msg, input_pfdo)
    else:
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, input_date_birth)


def input_pfdo(message):
    tID = message.chat.id
    data = message.text
    if data == "0":
        bot.send_message(tID, "Понял, ставлю прочерк")
        with connection.cursor() as cursor:
            cursor.execute("update users set cert_number = \"" +
                           "0" + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
        msg = bot.send_message(
            tID, "Теперь введи фамилию, имя и отчество одного из родителей")
        bot.register_next_step_handler(msg, input_parent_name)
    elif data.isdigit():
        with connection.cursor() as cursor:
            cursor.execute("update users set cert_number = \"" +
                           data + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
        bot.send_message(
            tID, "Хорошо, что у тебя есть сертификат ПФДО, он позволит обучаться в большем количестве секций")
        msg = bot.send_message(
            tID, "Напиши фамилию, имя и отчество одного из родителей через пробел")
        bot.register_next_step_handler(msg, input_parent_name)
    else:
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, input_pfdo)


def input_parent_name(message):
    tID = message.chat.id
    data = message.text
    if not checkName(data):
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, input_parent_name)
    else:
        with connection.cursor() as cursor:
            cursor.execute("update users set parent_firstname = \"" +
                           data.split(" ")[0] + "\" where tID = \"" + str(tID) + "\"")
            cursor.execute("update users set parent_lastname = \"" +
                           data.split(" ")[1] + "\" where tID = \"" + str(tID) + "\"")
            cursor.execute("update users set parent_patronymic = \"" +
                           data.split(" ")[2] + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
        msg = bot.send_message(
            tID, "Отправь рабочую электронную почту родителя")
        bot.register_next_step_handler(msg, input_email)


def input_email(message):
    tID = message.chat.id
    data = message.text
    with connection.cursor() as cursor:
            cursor.execute("update users set parent_email = \"" +
                           data + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
    # ПРОВЕРКА ПОЧТЫ
    msg = bot.send_message(
        tID, "Отправь мне местоположение своего дома, чтобы найти кружки поблизости")
    bot.register_next_step_handler(msg, get_location)

@bot.message_handler(content_types=["location"])
def get_location(message):
    # ДОБАВИТЬ В БАЗУ ДАННЫХ
    tID = message.chat.id
    data= str(message.location)
    posX = data[14:23]
    posY = data[37:45]
    with connection.cursor() as cursor:
            cursor.execute("update users set posX = \"" +
                           str(posX) + "\" where tID = \"" + str(tID) + "\"")
            cursor.execute("update users set posY = \"" +
                           str(posY) + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
    bot.send_message(tID, "Уже подбираю тебе кружки около твоего дома...")
    time.sleep(1)
    with connection.cursor() as cursor:
        cursor.execute("select kid_firstname, kid_lastname from users where tID = \"" + str(tID) + "\"")
        data = cursor.fetchall()
    bot.send_message(
        tID, "Ура! " + str(data[0][1]) + ", у тебя получилось зарегистрироваться!\nЧтобы начать искать кружки, мне нужно узнать, чем ты увлекаешься\nНапиши /quiz")

@bot.message_handler(commands=['quiz'])
def start_quiz(message):
    tID = message.chat.id
    with connection.cursor() as cursor:
        cursor.execute("select kid_firstname, kid_lastname from users where tID = \"" + str(tID) + "\"")
        data = cursor.fetchall()
    if data:
        bot.send_message(tID, "Давай узнаем о твоих увлечениях. Отвечай \"да\" или \"нет\"")
        msg = bot.send_message(tID, "Любишь заниматься спортом?")
        bot.register_next_step_handler(msg, pick_sport)
    else:
        bot.send_message(tID, "Ты ещё не зарегистрирован в ГосУслугах Дети, напиши /start")

def pick_sport(message):
    tID = message.chat.id
    answer = message.text
    if answer.lower() == "да":
        with connection.cursor() as cursor:
            cursor.execute("update users set categories = \"" +
                           "1" + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
            msg = bot.send_message(tID, "Как насчёт технологий IT?")
            bot.register_next_step_handler(msg, pick_it)
    elif answer.lower() == "нет":
        msg = bot.send_message(tID, "Как насчёт технологий IT?")
        bot.register_next_step_handler(msg, pick_it)
    else:
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, pick_sport)

def pick_it(message):
    tID = message.chat.id
    answer = message.text
    if answer.lower() == "да":
        with connection.cursor() as cursor:
            cursor.execute("update users set categories = CONCAT(categories, \"" +
                           "2" + "\") where tID = \"" + str(tID) + "\"")
            connection.commit()
        msg = bot.send_message(tID, "Увлекаешься рисованием?")
        bot.register_next_step_handler(msg, pick_painting)
    elif answer.lower() == "нет":
        msg = bot.send_message(tID, "Увлекаешься рисованием?")
        bot.register_next_step_handler(msg, pick_painting)
    else:
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, pick_it)


def pick_painting(message):
    tID = message.chat.id
    answer = message.text
    if answer.lower() == "да":
        with connection.cursor() as cursor:
            cursor.execute("update users set categories = CONCAT(categories,\"" +
                           "3" + "\") where tID = \"" + str(tID) + "\"")
            connection.commit()
        msg = bot.send_message(tID, "Увлекаешься рисованием?")
        bot.register_next_step_handler(msg, pick_chess)
    elif answer.lower() == "нет":
        msg = bot.send_message(tID, "Увлекаешься рисованием?")
        bot.register_next_step_handler(msg, pick_chess)
    else:
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, pick_painting)

def pick_chess(message):
    tID = message.chat.id
    answer = message.text
    if answer.lower() == "да":
        with connection.cursor() as cursor:
            cursor.execute("update users set categories = CONCAT(categories,\"" +
                           "4" + "\") where tID = \"" + str(tID) + "\"")
            connection.commit()
        msg = bot.send_message(tID, "Может любишь поиграть на музыкальных инструментах?")
        bot.register_next_step_handler(msg, pick_music)
    elif answer.lower() == "нет":
        msg = bot.send_message(tID, "Может любишь поиграть на музыкальных инструментах?")
        bot.register_next_step_handler(msg, pick_music)
    else:
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, pick_chess)

def pick_music(message):
    tID = message.chat.id
    answer = message.text
    if answer.lower() == "да":
        with connection.cursor() as cursor:
            cursor.execute("update users set categories = CONCAT(categories,\"" +
                           "4" + "\") where tID = \"" + str(tID) + "\"")
        connection.commit()
        msg = bot.send_message(tID, "Отлично, я запомнил все твои увлечения! Начинай выбирать, просто напиши /clubs")
    elif answer.lower() == "нет":
        msg = bot.send_message(tID, "Отлично, я запомнил все твои увлечения! Начинай выбирать, просто напиши /clubs")
    else:
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, pick_music)
