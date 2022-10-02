# import mysql.connector
#
# db = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='root',
#     database='fastapi_user_session_hw'
# )
#
# mycursor = db.cursor()
# mycursor.execute('USE fastapi_user_session_hw')
#
# select_query = """
# SELECT *
# FROM sessions
# WHERE token = 44#6|!1xas2nlg&vocvk2j5l&/#iy!l$;a3^$?va^#?6q6#1ojmx37/j.sg9&`53@1xu,v+e7e.-2?vwx.c4$,s$xlev!m/xqv7!.y#3?q^+@s,2/o,x&l99
# """
# mycursor.execute(select_query)
#
# for i in mycursor:
#     print(i[4])

# x =[
#     {
#         "creation_time": "2022-09-21 21:48:51.275426",
#         "id": 1,
#         "token": "44#6|!1xas2nlg&vocvk2j5l&/#iy!l$;a3^$?va^#?6q6#1ojmx37/j.sg9&`53@1xu,v+e7e.-2?vwx.c4$,s$xlev!m/xqv7!.y#3?q^+@s,2/o,x&l99",
#         "user_id": 1,
#         "ttl": "02:00:00"
#     }
# ]
# print(x[0]['ttl'])

from datetime import datetime, timedelta

# date_string = "2022-09-22 22:38:50.684320"
date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
date_object = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
delta = timedelta(hours=date_object.hour, minutes=date_object.minute, seconds=date_object.second)
ttl = datetime.strptime("00:02:00", '%H:%M:%S')
delta2 = timedelta(hours=ttl.hour, minutes=ttl.minute, seconds=ttl.second)
# print(date_object)
# print(delta)
# print(delta2)
# print(date_object + delta2)

print(datetime.now().replace(microsecond=0))
print(type(datetime.now().replace(microsecond=0)))