@bot.message_handler(commands=['showprofile'])
def showProfile(message):
    tID = message.chat.id
    bot.send_message(tID, "Информация из профиля:")
    with connection.cursor() as cursor:
        cursor.execute("select * from users where tID = \"" + str(tID) + "\"")
        data = cursor.fetchall()
        dict = {"1":", Спорт", "2":", Технологии IT","3":", Рисование","4":", Шахматы","5":", Музыка"}
        cat = ""
        for a in data[0][13]:
            cat = cat + dict[a]
    
    info = "Твоё ФИО: " + str(data[0][0]) + " " + str(data[0][1]) + " " + data[0][2] + "\n" + \
        "Твоя дата рождения: " + data[0][10] + "\n" + \
        "Номер сертификата ПФДО: " + data[0][9] + "\n" + \
        "ФИО Родителя: " + str(data[0][3]) + " " + str(data[0][4]) + " " + data[0][5] + "\n" + \
        "Электронная почта: " + data[0][8] + "\n" + \
        "Твои интересы: " + cat[2:]
    bot.send_message(tID, info)
