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
                    user_progress[user_id]['answers'][user_progress[user_id]['step']] == message_text
                else:
                    user_progress[user_id]['answers'][user_progress[user_id]['step']] == list(map(int, message_text.split()))
                user_progress[user_id]['step'] = len(user_progress[user_id]['answers'])
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
            try:
                if tests[test_id]['answers'][user_progress[user_id]['step'] - 1] == 0:
                    user_progress[user_id]['answers'].append(message_text)
                else:
                    user_progress[user_id]['answers'].append(list(map(int, message_text.split())))
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

            except TypeError as e:
                print(e)
                text = 'Возникла ошибка, попробуй снова.'


    send(user_id, text, ['Вернуться к вопросу', 'Завершить прохождение'])
    print(text)
    print(tests)
    print(user_progress)

    return(ret)