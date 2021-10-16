import pymysql
from func.geoloc import distance_calc

def sorting(tag):
    with connection.cursor() as cur:
        cur.execute('select * from clubs')
        data = cur.fetchall()
    if tag == 1:
        data = sorted(data, key=lambda x: x[tag])
    else:
        data = sorted(data, key=lambda x: distance_calc(x[2], x[3], tag[0], tag[1]))
    return data