import pymysql


def take_base_clubs(listt):
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="1111",
        database="botDB"
    )
    with connection.cursor() as cur:
        cur.execute('select * from clubs')
        data = list(cur.fetchall())
    data = [list(i) for i in data]
    ans = ''
    print(data)
    print(listt)
    for i in range(len(listt)):
        for j in range(len(data)):
            if data[j][0] == listt[i][0]:
                num = j
                break
        ans += (str(num + 1) + '. ' + listt[i][0] + '\n')
        print(ans)
    return ans