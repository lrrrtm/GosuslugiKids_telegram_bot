@bot.message_handler(commands=['edit_profile'])
def showProfile(message):
    tID = message.chat.id
    bot.send_message(tID, "Данные из профиля:")
    with connection.cursor() as cursor:
        cursor.execute("select * from users where tID = \"" + str(tID) + "\"")
        data = cursor.fetchall()
        dict = {"1":", Спорт", "2":", Технологии IT","3":", Рисование","4":", Шахматы","5":", Музыка"}
        cat = ""
        for a in data[0][13]:
            cat = cat + dict[a]
    
    info = "1. Твоё ФИО: " + str(data[0][0]) + " " + str(data[0][1]) + " " + data[0][2] + "\n" + \
        "2. Твоя дата рождения: " + data[0][10] + "\n" + \
        "3. Номер сертификата ПФДО: " + data[0][9] + "\n" + \
        "4. ФИО Родителя: " + str(data[0][3]) + " " + str(data[0][4]) + " " + data[0][5] + "\n" + \
        "5. Электронная почта: " + data[0][8] + "\n" + \
        "6. Твои интересы: " + cat[2:]
    bot.send_message(tID, info)
    msg = bot.send_message(tID, "Выбери номер строки, которую хочешь изменить")
    bot.register_next_step_handler(msg, pick_line)

def pick_line(message):
    tID = message.chat.id
    num = message.text
    if num.isdigit() and len(num) == 1 and int(num) in range(1,7):
        num = int(num)
        if num == 1:
            msg = bot.send_message(tID, "Введи свою фамилию, имя и отчество через пробел")
            bot.register_next_step_handler(msg, commit_kid_name)
        elif num == 2:
            msg = bot.send_message(tID, "Введи свою дату рождения в формате ДД.ММ.ГГГГ")
            bot.register_next_step_handler(msg, commit_birth_date)
        elif num == 3:
            msg = bot.send_message(tID, "Введи номер сертификата ПФДО, если его нет, введи 0")
            bot.register_next_step_handler(msg, commit_pfdo_num)

        elif num == 4:
            msg = bot.send_message(tID, "Введи фамилию, имя и отчество родителя через пробел")
            bot.register_next_step_handler(msg, commit_parent_name)

        elif num == 5:
            msg = bot.send_message(tID, "Введи действующую электронную почту родителя")
            bot.register_next_step_handler(msg, commit_parent_email)

        elif num == 6:
            msg = bot.send_message(tID, "Введи цифры направлений, которые тебе интересны, например, 124\n1. Спорт\n2. Технологии IT\n3. Рисование\n4. Шахматы\n5. Музыка")
            bot.register_next_step_handler(msg, commit_categories)
        else:
            msg = bot.send_message(tID, incorrect_input_text)
            bot.register_next_step_handler(msg, pick_line)

def commit_kid_name(message):
    tID = message.chat.id
    data = message.text
    if not checkName(data):
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, commit_kid_name)
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
            tID, "Твоё ФИО успешно обновлено")

def commit_birth_date(message):
    tID = message.chat.id
    data = message.text
    if checkDate(data):
        with connection.cursor() as cursor:
            cursor.execute("update users set birth_date = \"" +
                           data + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
        bot.send_message(tID, "Твоя дата рождения обновлена")
    else:
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, commit_birth_date)

def commit_pfdo_num(message):
    tID = message.chat.id
    data = message.text
    if data == "0":
        with connection.cursor() as cursor:
            cursor.execute("update users set cert_number = \"" +
                           "0" + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
        bot.send_message(tID, "Твой номер сертификата ПФДО обновлён")
    elif data.isdigit():
        with connection.cursor() as cursor:
            cursor.execute("update users set cert_number = \"" +
                           data + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
        bot.send_message(tID, "Твой номер сертификата ПФДО обновлён")
    else:
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, commit_pfdo_num)

def commit_parent_name(message):
    tID = message.chat.id
    data = message.text
    if not checkName(data):
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, commit_parent_name)
    else:
        with connection.cursor() as cursor:
            cursor.execute("update users set parent_firstname = \"" +
                           data.split(" ")[0] + "\" where tID = \"" + str(tID) + "\"")
            cursor.execute("update users set parent_lastname = \"" +
                           data.split(" ")[1] + "\" where tID = \"" + str(tID) + "\"")
            cursor.execute("update users set parent_patronymic = \"" +
                           data.split(" ")[2] + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
        bot.send_message(tID, "ФИО твоего родителя обновлено")

def commit_parent_email (message):
    tID = message.chat.id
    data = message.text
    with connection.cursor() as cursor:
            cursor.execute("update users set parent_email = \"" +
                           data + "\" where tID = \"" + str(tID) + "\"")
            connection.commit()
    bot.send_message(tID, "Электронная почта твоего родителя обновлена")
    # ПРОВЕРКА ПОЧТЫ

def commit_categories(message):
    tID = message.chat.id
    data = message.text
    if not data.isdigit():
        msg = bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, commit_categories)
    else:
        with connection.cursor() as cursor:
            cursor.execute("update users set categories = \"" +
                            data + "\" where tID = \"" + str(tID) + "\"")
            connection.commit
        bot.send_message(tID, "Твой список интересов обновлён")