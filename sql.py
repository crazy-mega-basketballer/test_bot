from getpass import getpass
from mysql.connector import connect, Error
from enc_dec import *

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
        c += f'{s}, '
    c = c[:-2]
    for s in values:
        if type(s) == str:
            v += f'"{s}", '
        elif type(s) == int:
            v += f'{s}, '

    v = v[:-2]

    try:
        with connect(
            host="localhost",
            user="root",
            password=f"{PAS}",
            database="test_bot",
        ) as connection:
            with connection.cursor() as cursor:
                comand = f'''insert {table} ({c})
values ({v})'''
                print(comand)
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



def insert_test(user_id, name, questions, answers, true = None):
    enc = encryption(questions, answers, true)
    insert('tests', ['user_id', 'name', 'text', 'cipher'], [user_id, name, enc[0], enc[1]])



def select(table, colums = '*', where = ''):
    ret = []
    try:
        with connect(
            host='localhost',
            user='root',
            password=f"{PAS}",
            database='test_bot',
        ) as connection:
            with connection.cursor() as cursor:
                comand = f'''SELECT {colums} FROM {table}'''
                if where != '':
                    comand += f'''
WHERE {where}'''
                cursor.execute(comand)
                ret = cursor.fetchall()
    except Error as e:
        print('Eror: ', e)
    
    return(ret)

#dima gey loh pidor evrey i tak dalee