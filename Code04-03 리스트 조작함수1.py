## 특정값의 모든 위치를 출력하는 프로그램

import random

myList = [random.randint(1,5) for _ in range (10)]

NUMBER = 5
print(myList)
index = 0

for i in range(myList.count(NUMBER)) :
        index = myList.index(NUMBER, index)
        print(index)
        index += 1

