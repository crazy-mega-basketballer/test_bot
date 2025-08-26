from sql import *
from enc_dec import *
from connect import *

tests = {}
user_progress = {}
def passing(user_id, test_id, message_text):
    ret = False
    if test_id not in tests:
        test = select('tests', 'text, cipher', f'test_id = {test_id}')
        test = decryption(test[0][0], test[0][1])
        if (test[2]):
            tests.update({test_id : {
                'pas_now' : 0,
                'questions' : test[0],
                'answers' : test[1],
                'true' : test[2],
            }})
        else:
            tests.update({test_id : {
                'pas_now' : 0,
                'questions' : test[0],
                'answers' : test[1],
            }})

    if user_id not in user_progress:
        tests[test_id]['pas_now'] += 1
        user_progress.update({user_id : {
            'step' : 0,
            'answers' : []
        }})
        send(user_id, f'Вопросов: {len(tests[test_id]['questions'])}\nудачи не заебаться')
    
    print(tests)
    print(user_progress)
    print()

    text = f''''''

    if (message_text not in ['Вернуться к вопросу', 'Завершить прохождение']):
        if (user_progress[user_id]['step'] == -1):
            try:
                user_progress[user_id]['step'] = int(message_text) - 1
                question = tests[test_id]['questions'][user_progress[user_id]['step']]
                text += f'''Вопрос {message_text}/{len(tests[test_id]['questions'])}

{question}'''
                if (tests[test_id]['answers'][user_progress[user_id]['step']] == 0):
                    text += f'''

    ***Развернутый ответ'''
                    
                else:
                    text += f'''

Варианты ответов:'''
                    for ans_num in range(len(tests[test_id]['answers'][user_progress[user_id]['step']])):
                        text += f'''
    {ans_num + 1}) {tests[test_id]['answers'][user_progress[user_id]['step']][ans_num]}'''

            except TypeError as e:
                print(e)
                user_progress[user_id]['step'] = -1
                text = 'Возникла ошибка, попробуй снова. На какой вопрос ты хочешь ответить? (укажи только номер вопроса)'
        
        elif (len(user_progress[user_id]['answers']) > user_progress[user_id]['step'] and len(user_progress[user_id]['answers']) != 0):
            print(1)
            try:
                if tests[test_id]['answers'][user_progress[user_id]['step']] == 0:
                    user_progress[user_id]['answers'][user_progress[user_id]['step']] = message_text
                else:
                    user_progress[user_id]['answers'][user_progress[user_id]['step']] = list(map(int, message_text.split()))
                user_progress[user_id]['step'] = len(user_progress[user_id]['answers'])

                if (user_progress[user_id]['step'] < len(tests[test_id]['questions'])):
                    text += f'''Вопрос {user_progress[user_id]['step'] + 1}/{len(tests[test_id]['questions'])}
    
    {tests[test_id]['questions'][user_progress[user_id]['step']]}'''
                    if (tests[test_id]['answers'][user_progress[user_id]['step']] == 0):
                        text += f'''
    
        ***Развернутый ответ'''
                        
                    else:
                        text += f'''

    Варианты ответов:'''
                        for ans_num in range(len(tests[test_id]['answers'][user_progress[user_id]['step']])):
                            text += f'''
        {ans_num + 1}) {tests[test_id]['answers'][user_progress[user_id]['step']][ans_num]}'''
                            
                    user_progress[user_id]['step'] += 1
                else:
                    if (len(user_progress[user_id]['answers']) != len(tests[test_id]['questions'])):
                        text = 'Возникла ошибка, попробуй снова.'

                    else:
                        user_progress[user_id]['step'] = -2
                        text = f'''Хотите завершить прохождение?'''
    
            except TypeError as e:
                print(e)
                text = 'Возникла ошибка, попробуй снова.'
        
        elif (len(user_progress[user_id]['answers']) == user_progress[user_id]['step'] and len(user_progress[user_id]['answers']) < len(tests[test_id]['questions'])):
            print(2)
            text += f'''Вопрос {user_progress[user_id]['step'] + 1}/{len(tests[test_id]['questions'])}

{tests[test_id]['questions'][user_progress[user_id]['step']]}'''
            print(3)
            if (tests[test_id]['answers'][user_progress[user_id]['step']] == 0):
                text += f'''

    ***Развернутый ответ'''
                    
            else:
                text += f'''

Варианты ответов:'''
                for ans_num in range(len(tests[test_id]['answers'][user_progress[user_id]['step']])):
                    text += f'''
    {ans_num + 1}) {tests[test_id]['answers'][user_progress[user_id]['step']][ans_num]}'''
            user_progress[user_id]['step'] += 1

        elif (len(user_progress[user_id]['answers']) == user_progress[user_id]['step'] - 1):
            print(4)
            print('+++++++++++')
            print(tests)
            print(user_progress)
            print('+++++++++++')
            try:
                print(5)
                if tests[test_id]['answers'][user_progress[user_id]['step'] - 1] == 0:
                    user_progress[user_id]['answers'].append(message_text)
                else:
                    user_progress[user_id]['answers'].append(list(map(int, message_text.split())))
                print(7)
                if (user_progress[user_id]['step'] < len(tests[test_id]['questions'])):
                        
                    text += f'''Вопрос {user_progress[user_id]['step'] + 1}/{len(tests[test_id]['questions'])}
    
    {tests[test_id]['questions'][user_progress[user_id]['step']]}'''
                    print(8)
                    if (tests[test_id]['answers'][user_progress[user_id]['step']] == 0):
                        text += f'''
    
        ***Развернутый ответ'''
                        
                    else:
                        text += f'''
    
    Варианты ответов:'''
                        for ans_num in range(len(tests[test_id]['answers'][user_progress[user_id]['step']])):
                            text += f'''
        {ans_num + 1}) {tests[test_id]['answers'][user_progress[user_id]['step']][ans_num]}'''
                    print(9)
                    user_progress[user_id]['step'] += 1
                else:
                    print(11)
                    if (len(user_progress[user_id]['answers']) != len(tests[test_id]['questions'])):
                        text = 'Возникла ошибка, попробуй снова.'

                    else:
                        user_progress[user_id]['step'] = -2
                        text = f'''Хотите завершить прохождение?'''

            except TypeError as e:
                print(e)
                print(6)
                text = 'Возникла ошибка, попробуй снова.'
    
    elif (message_text == 'Вернуться к вопросу'):
        user_progress[user_id]['step'] = -1
        text = 'Введите номер вопроса, на который хотите ответить заново. (можно перезаписать ответ только на предыдущие вопросы)'
    
    elif (message_text == 'Завершить прохождение'):
        if (len(user_progress[user_id]['answers']) == len(tests[test_id]['questions']) and user_progress[user_id]['step'] == -2):
            text = 'Браво, ты справился! (наверное)'
            answers = ''
            for ans in user_progress[user_id]['answers']:
                if (type(ans) == str):
                    answers += f"'{ans}'~|~"
                else:
                    for i in ans:
                        answers += f'{i} '
                    answers = answers[:-1]
                    answers += f'~|~'
            answers = answers[:-3]

            if len(select('passings', where = f'tester_id = "{user_id}" and test_id = {test_id}')) > 0:
                try:
                    with connect(
                        host="localhost",
                        user="root",
                        password=f"{PAS}",
                        database="test_bot",
                    ) as connection:
                        with connection.cursor() as cursor:
                            comand = f'''UPDATE passings
SET answers = '{answers}'
WHERE tester_id = "{user_id}" and test_id = {test_id};'''
                            cursor.execute(comand)
                            connection.commit()
                except Error as e:
                    print('Eror: ', e)

            else:
                insert('passings', ['tester_id', 'test_id', 'answers'], [str(user_id), int(test_id), answers])

            user_progress.pop(user_id, None)
            tests[test_id]['pas_now'] -= 1
            if tests[test_id]['pas_now'] == 0:
                tests.pop(test_id, None)
            ret = True
        
        elif (len(user_progress[user_id]['answers']) < len(tests[test_id]['questions']) and user_progress[user_id]['step'] != -2):
            text = 'Ты не ответил на все вопросы, похуй?'
            for answer in range(len(user_progress[user_id]['answers']), len(tests[test_id]['questions'])):
                if (tests[test_id]['answers'][answer] == 0):
                    user_progress[user_id]['answers'].append('')
                else:
                    user_progress[user_id]['answers'].append([0])
            user_progress[user_id]['step'] = -2

    send(user_id, text, ['Вернуться к вопросу', 'Завершить прохождение'])
    print(text)
    print(tests)
    print(user_progress)
    print('----------------------------')
    return(ret)