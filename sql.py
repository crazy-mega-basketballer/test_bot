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

def decryption(text, cipher):
    cipher = list(map(int, cipher.split(',')))
    questions = []
    answers = []
    indx = 0
    piece = 0

    length = cipher[piece]
    for l in cipher[piece + 1:piece + 1 + length]:
        questions.append(text[indx:indx + l])
        indx += l
    piece += length + 1
    
    while piece < len(cipher):
        length = cipher[piece]
        if length == 0:
            answers.append(0)
            piece += 1
        else:
            answer = []
            for l in cipher[piece + 1:piece + 1 + length]:
                answer.append(text[indx:indx + l])
                indx += l
            answers.append(answer)
            piece += length + 1
    
    return([questions, answers])


def encryption(questions, answers, true = None):

    cipher = f'{len(questions)},'
    for question in questions:
        cipher += f'{len(question)},'
    for answer in answers:
        if (answer == 0):
            cipher += f'0,'
        else:
            cipher += f'{len(answer)},'
            for variant in answer:
                cipher += f'{len(variant)},'
    cipher = cipher[:-1]

    text = ''
    for q in questions:
        text += q
    for a in answers:
        if a != 0:
            for answer in a:
                text += answer

    return([text, cipher])


def insert_test(questions, answers, true = None):
    enc = encryption(questions, answers, true)
    denc = decryption(enc[0], enc[1])
    print(enc)
    print(denc)