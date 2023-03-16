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
# db.commit()
# mycursor.execute(f"INSERT INTO money (user_id, balance, credit_balance)"
#                  f" VALUES ('1', '111', '123')")


# token = "vp;1>5k*/1ljqj6j.3/;`$e.g~3d/&u.?;!h14/*^/4q38vg~nhjvngpoad:d~:lw3ah<a+y;&$!ws>ke&m3e73w$9p*4q`@:1m4ok|sd1?`6`?qhnu.ghgi"
# mycursor.execute(f"INSERT INTO sessions (user_id, token, creation_time, ttl)"
#                  f" VALUES ('1', '{token}', '2022-10-06 22:41:30.981246', '00:02:00')")
# db.commit()


# @router.post('/user', status_code=status.HTTP_201_CREATED)
# def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
#     new_entry = models.Users(user_name=request.user_name, age=request.age,
#                              sex=request.sex, phone_number=request.phone_number,
#                              password=Hash.bcrypt(request.password))
#     db.add(new_entry)
#     db.commit()
#     db.refresh(new_entry)
#     return new_entry


# mycursor.execute("INSERT INTO contact_groups(group_id, group_name)"
#                  "VALUES"
#                  "(1, 'not assigned'),"
#                  "(2, 'work'),"
#                  "(3, 'family')")
# mycursor.execute("INSERT INTO contacts(user_id, name, phone, group_name)"
#                  "VALUES"
#                  "(1, 'a', '12345', 'not assigned'),"
#                  "(1, 'b', '12344', 'not assigned'),"
#                  "(1, 'c', '12346', 'family')")
# db.commit()

# x = """
#     SELECT contacts.name, contacts.group_id, contact_groups.group_name
#     FROM contacts
#     INNER JOIN contact_groups
#     ON contacts.group_id = contact_groups.group_id
#     WHERE contacts.group_id = 1
#     """
# mycursor.execute(x)
# mycursor = mycursor.fetchall()
# for x in mycursor:
#     print(x)
# db.close()

# x = text(
#     f"SELECT contacts.name, contacts.group_id, contact_groups.group_name FROM contacts INNER JOIN contact_groups ON contacts.group_id = contact_groups.group_id WHERE contacts.group_id = 1"
#     )
# return db.execute(x).all()

# return db.query(Contacts.name, ContactGroups.group_name).join(ContactGroups).filter(Contacts.group_id == 1).all()

# x = """
#     SELECT contacts.name, contacts.search_hashed_id,
#     search_hashed_id.search_id, search_hashed_id.field_name, search_hashed_id.field_value
#     FROM contacts
#     INNER JOIN search_hashed_id
#     ON contacts.search_hashed_id = search_hashed_id.search_id
#     """
#
# mycursor.execute(x)
# mycursor = mycursor.fetchall()
# for x in mycursor:
#     print(x)
# db.close()