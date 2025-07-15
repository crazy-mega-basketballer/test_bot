def encryption(questions, answers, true):

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

    if true:
        for ans in true:
            for a in ans:
                text += f'{a} '
            text = text[:-1] + ','
        text = text[:-1]
    return([text, cipher])



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
    
    true = []
    if indx < len(text):
        text = text[indx:].split(',')
        for ans in text:
            if ' ' in ans:
                true.append(list(map(int, ans.split())))
            else:
                true.append([int(ans)])

    return([questions, answers, true])