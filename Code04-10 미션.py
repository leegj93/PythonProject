## Mission

import random

data = []
i, k = 0, 0

if __name__== "__main__":
    for i in range(0,10):
        tmp = hex(random.randrange(0,100000))
        data.append(tmp)

    print('정렬 전 데이터 : ', end = '')
    [print(num, end=' ') for num in data]
## 선택 정렬
    for i in range(0, len(data) -1):
        for k in range(i+1, len(data)):
            if int(data[i], 16)> int(data[k], 16):
                tmp = data[i]
                data[i] = data[k]
                data[k] = tmp
    print('\n정렬 후 데이터 : ', end='')
    [print(num, end=' ')for num in data]

## 버블 정렬
    for i in range(len(data)):
        for k in range(0, len(data)-i-1):
            if int(data[k], 16) > int(data[k+1], 16):
                data[k], data[k+1] = data[k+1], data[k]
    print('\n정렬 후 데이터 : ', end='')
    [print(num, end=' ')for num in data]


## 퀵정렬
    # for i in range(len(data)):