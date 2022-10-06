import mysql.connector
from core.hashing import Hash

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='fastapi_homework1'
)

mycursor = db.cursor()

mycursor.execute('USE fastapi_homework1')

# insert_user_table_query = """
# INSERT INTO USERS(user_id, balance, credit_balance)
# VALUES
# ('user1', 35, male, 111222333, %s)
# """
#
# insert_money_table_query = """
# INSERT INTO money(user_id, balance, credit_balance)
# VALUES
# (1, '111', '123');
# """

# mycursor.execute(f"INSERT INTO users (user_name, age, sex, phone_number, password)"
#                  f" VALUES ('user1', '18', 'male', '1112223333', '{Hash.bcrypt('password1')}')")
# mycursor.execute(f"INSERT INTO money (user_id, balance, credit_balance)"
#                  f" VALUES ('1', '111', '123')")
token = "@.8,#q9loj:5l;##yd?@yy^d~2&<1?#v$$gs@8&,v~3pdk365;3y<li;d22p6!:|chcdwj8~k->cvd,l~yg!u3>x$vk@s.qj92##k-e~~k?xs/!36/,x26w;"
mycursor.execute(f"INSERT INTO sessions (user_id, token, creation_time, ttl)"
                 f" VALUES ('1', '{token}', '2022-10-06 22:41:30.981246', '00:02:00')")
db.commit()


# @router.post('/user', status_code=status.HTTP_201_CREATED)
# def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
#     new_entry = models.Users(user_name=request.user_name, age=request.age,
#                              sex=request.sex, phone_number=request.phone_number,
#                              password=Hash.bcrypt(request.password))
#     db.add(new_entry)
#     db.commit()
#     db.refresh(new_entry)
#     return new_entry
