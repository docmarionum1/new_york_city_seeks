a = ['execute', 'test', 'scripts', 'i++', 'for', 'new', 'york', 'city', 'through', '-through', 'cyber', 'i++', 'command', 'with', '-with', '-command', 'i--', '-cyber', '-city', 'budgeting', 'and', 'i++', 'procurement', 'systems', 'i++']

a = ['Ensure', 'staff', 'receive', 'i++', 'the', 'training', 'and', 'support', 'to', 'i++', 'the', 'enterprise', '-enterprise', 'project', 'to', '-to', '-project', 'chief', 'of', 'staff', '-staff', '-of', '-chief', '-the', 'i--', '-to', 'in', 'i++', 'MS', 'Dynamics', '-dynamics', '-ms', 'i--', '-in', 'IT', 'i++', 'operations', '-operations', 'i--', '-it', '-support', '-and', '-training', '-the', 'i--', '-receive', '-staff', 'that', 'standard', 'i++', 'processes', 'are', 'used', 'by', 'the', 'i++', 'mayor', 'and', 'the', '-the', '-and', '-mayor', 'i--', '-the', 'field', 'i++', 'code', '-code', 'i--', '-field', '-by', '-used', '-are', 'to', 'review', 'all', 'i++', 'defects', 'and', 'work', 'styles', 'i++']

h = [[],[],[]]
i = 0

import os
import time
import random

def print_haiku():
    os.system('cls')
    text = '\n'.join([' '.join(r) for r in h])
    print(text)
    time.sleep(random.random()/10)

for w in a:
    #if w != 'i++' and w != 'i--':
    #    h[i].append(w)
    if w == 'i++':
        i += 1
    elif w == 'i--':
        i -= 1
    elif w[0] == '-':
        while (len(h[i][-1]) > 0):
            h[i][-1] = h[i][-1][:-1]
            print_haiku()
        h[i].pop()
    else:
        h[i].append('')
        for c in w:
            h[i][-1] += c
            print_haiku()
        
        
        
    
    
    
        
    
        
    print()
    
    time.sleep(random.random())
        