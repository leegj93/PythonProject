# i, k = 0, 0
#
# for i in range(2, 10, 1) :
#     for k in range(1, 10, 1):
#         print( i , '*', k, '=', i*k)

## 10 X 10 크기의 숫자를 예쁘게 출력해라 ##

import random
import random as rd
from random import randrange, randint
# count = 0
for _ in range(10) :
    for _ in range(10) :
        num = randint(0,99)
        print(" %2d " % (num), end ='')
        # count += 1
    print()