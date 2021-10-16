def input_email(message):
    tID = message.chat.id
    data = message.text
    if not validate_email(data, check_mx=True):
        msg=bot.send_message(tID, incorrect_input_text)
        bot.register_next_step_handler(msg, commit_parent_email)
    else: 
        with connection.cursor() as cursor:
                cursor.execute("update users set parent_email = \"" +
                            data + "\" where tID = \"" + str(tID) + "\"")
                connection.commit()
        msg = bot.send_message(
            tID, "Отправь мне местоположение своего дома, чтобы найти кружки поблизости")
        bot.register_next_step_handler(msg, get_location)