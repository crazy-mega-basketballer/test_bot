from itertools import *
from json import *

def prov(a):
    return(eval(a))

def variable(name):
    for s in product('01', repeat = len(name)):
        i = ''.join(s)
        var = ''
        for c in range(len(i)):
            if i[c] == '0':
                var += (name[c]).lower()
            else:
                var += (name[c]).upper()
        print(var)
        input()

dump_mes = set()
def for_dump(m):
    if (m.json['text'] not in dump_mes):
        with open('mes.json', 'w', encoding="utf-8") as file:
            to_dump = {f'{m.text}': m.json}
            print(to_dump)
            dump(to_dump, file, indent=4)
            dump_mes.add(m.json['text'])

