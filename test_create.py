from connect import *

create_now = set()
tests = {}
def create_test(m = 0, call = 0):
    if m:
        user_id = m.from_user.id
        str_user_id = str(user_id)
        text = m.text
    if (user_id not in create_now):
        create_now.add(user_id)
        tests.update({
            str_user_id : [text, 0, [], [], 1, 0]
        })
        send(user_id, 'Будут ли в твоем тесте правильные ответы?', ['Да', 'Нет'])
    else:
        if (tests[str_user_id][1] == 0):
            if (text == 'Да'):
                tests[str_user_id][1] = 1
                tests[str_user_id].append([])
            else: tests[str_user_id][1] = 2
            send(user_id, 'Напишите вопрос:')
        else:
            if (tests[str_user_id][4] and text not in ['Добавить вопрос', 'Завершить создание']):
                tests[str_user_id][2].append(text)
                tests[str_user_id][4] = 0
                send(user_id, 'Выберите действие:', ['Добавить ответы', 'Развернутый ответ'])
            else:
                if (len(tests[str_user_id][2]) > len(tests[str_user_id][3]) and tests[str_user_id][1] != 3):
                    if (text == 'Развернутый ответ'):
                        tests[str_user_id][3].append(0)
                        tests[str_user_id][4] = 1
                        if (tests[str_user_id][1] == 1):
                            tests[str_user_id][6].append(0)
                        send(user_id, 'Напишите следующий вопрос или завершите создание теста, написав "Завершить создание"', ['Завершить создание'])
                    else:
                        send(user_id, 'Отправляйте ответы отдельными сообщениям. Если зохотети добавить вопрос или завершить создание, нажмите на соответствующую кнопку', ['Добавить вопрос', 'Завершить создание'])  
                        tests[str_user_id][3].append([])
                elif (text not in ['Добавить вопрос', 'Завершить создание'] and tests[str_user_id][5] == 0 and tests[str_user_id][1] != 3):
                    tests[str_user_id][3][-1].append(text)
                else:
                    if (text == 'Добавить вопрос' or tests[str_user_id][5]):
                        if (len(tests[str_user_id][3][-1]) == 0):
                            tests[str_user_id][3][-1] = 0
                            tests[str_user_id][4] = 1
                            tests[str_user_id][5] = 0
                            if (tests[str_user_id][1] == 1):
                                tests[str_user_id][6].append(0)
                            send(user_id, 'Напишите следующий вопрос или завершите создание теста, написав "Завершить создание"', ['Завершить создание'])
                        else:
                            if (tests[str_user_id][1] == 1 and len(tests[str_user_id][3]) > len(tests[str_user_id][6]) and tests[str_user_id][5] == 0):
                                send(user_id, 'Сначала укажи номер правильного ответа.\n\n(нумерация идет с первого,если ответов несколько, но напиши их через пробел: "1 2 3")')
                                tests[str_user_id][5] = 1
                            elif (tests[str_user_id][1] == 1 and len(tests[str_user_id][3]) > len(tests[str_user_id][6]) and tests[str_user_id][5] == 1):
                                ans = list(map(int, text.split()))
                                tests[str_user_id][6].append(ans)
                                tests[str_user_id][4] = 1
                                tests[str_user_id][5] = 0
                                send(user_id, 'Напишите следующий вопрос или завершите создание теста, написав "Завершить создание"', ['Завершить создание'])
                    else:
                        tests[str_user_id][4] = 0
                        tests[str_user_id][5] = 0
                        tests[str_user_id][1] = 3
                        if (len(tests[str_user_id][3][-1]) == 0):
                            tests[str_user_id][3][-1] = 0
                            if (tests[str_user_id][1] == 1):
                                tests[str_user_id][6].append(0)
                             

                        
                    
    print(tests)