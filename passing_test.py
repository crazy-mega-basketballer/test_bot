from sql import *
from enc_dec import *
from connect import *

tests = {}
user_progress = {}
def passing(user_id, test_id):
    ret = False

    if test_id not in tests:
        test = select('tests', 'text, cipher', f'test_id = {test_id}')
        test = decryption(test[0][0], test[0][1])

        if (test[2]):
            tests.update({test_id : {
                'pas_now' : 1,
                'questions' : test[0],
                'answers' : test[1],
                'true' : test[2],
            }})
        else:
            tests.update({test_id : {
                'pas_now' : 1,
                'questions' : test[0],
                'answers' : test[1],
            }})

        user_progress.update({user_id : {
            'step' : 0,
            'anwers' : []
        }})
        
        send(id, text, buttons = [], r = 1, t = 1)

    else:
        if user_id not in user_progress:
            tests[test_id]['pas_now'] += 1
            user_progress.update({user_id : {
                'step' : 0,
                'anwers' : []
            }})
        
        else:
            a = 1
    
    print(tests)
    print(user_progress)
    return(ret)