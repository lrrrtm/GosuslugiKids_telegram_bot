import pymysql
from func.geoloc import distance_calc


def take_info_clubs(id, num):
    ans = ''
    connection = pymysql.connect(
        host='localhost',
        database="botDB",
        user="root",
        password="1111"

    )
    with connection.cursor() as cursor:
        cursor.execute("select * from users where tID = {}".format(id))
        data_user = cursor.fetchall()
    with connection.cursor() as cursor:
        cursor.execute("select * from clubs")
        data = cursor.fetchall()
    ans += ('Название: ' + data[num - 1][0] + '\n')
    ans += ('Описание: ' + data[num - 1][4] + '\n')
    if data[num - 1][1] == "0":
        ans += ('Стоимость обучения: ' + "бесплатно" + '\n')
    else:
        ans += ('Стоимость обучения: ' + data[num - 1][1] + ' руб.\n')
    print(data_user[0][11], data_user[0][12])
    ans += ('Расстояние: ' + str(distance_calc(data_user[0][11], data_user[0][12], data[num-1][2], data[num-1][3])) + ' км')
    return [ans, [data[num-1][2], data[num-1][3]]]