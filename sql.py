from getpass import getpass
from mysql.connector import connect, Error

PATH = 'C:\\Users\\basda\\OneDrive\\Рабочий стол\\password.txt'
PAS = open(PATH).readline()

'''insert users (user_id, username)
values ("1967855723", 'huy')

truncate table users

select * from users'''

"""try:
    with connect(
        host="localhost",
        user="root",
        password= f"{PAS}",
        database="test_bot",
    ) as connection:
        with connection.cursor() as cursor:
            comand = '''
CREATE TABLE users(
user_id VARCHAR(15) PRIMARY KEY,
username VARCHAR(64),
friends VARCHAR(300)
);
'''
            cursor.execute(comand)
            connection.commit()
except Error as e:
    print("Eror: ", e)"""



def insert(table, colums, values):
    c, v = '', ''
    for s in colums:
        c += s+', '
    c = c[:-1]
    for s in values:
        v += s+', '
    v = v[:-1]

    try:
        with connect(
            host="localhost",
            user="root",
            password=f"{PAS}",
            database="test_bot",
        ) as connection:
            with connection.cursor() as cursor:
                comand = f'''insert {table} ({c})
values ("1967855723", 'huy')'''
                cursor.execute(comand)
                connection.commit()
    except Error as e:
        print('Eror: ', e)



def start(m):
    user_id = m.from_user.id
    username = m.from_user.username
    ret = 0
    try:
        with connect(
            host='localhost',
            user='root',
            password=f"{PAS}",
            database='test_bot',
        ) as connection:
            with connection.cursor() as cursor:
                comand = f'''SELECT username FROM users
                WHERE user_id = {user_id}'''

                cursor.execute(comand)
                answer = cursor.fetchall()

                if (len(answer) == 0):
                    comand = f'''insert users (user_id, username)
values ("{user_id}", "{username}")'''
                    cursor.execute(comand)
                    connection.commit()

                    ret = 1
    
    except Error as e:
        print('Eror: ', e)

    return(ret)