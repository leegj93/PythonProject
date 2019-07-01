# ## 4개의 랜덤한 숫자를 리스트에 저장한 후, 합계를 계산하자
# import random
# SIZE = 10
# ## 메모리 확보 개념(타 언어 스타일) ##
# aa = [] #빈 리스트 준비
#
#
# for i in range(SIZE) :
#     aa.append(0)
#
# ## 메모리에 필요한 값 대입 ---> 파일 읽기
#
# for i in range(4):
#     num= random.randint(0,99)
#     aa[i] = num
#
# ## 메모리 처리/조작/연산  ---> 알고리즘(컴퓨터 비전, 영상처리)
# sum= 0
# for i in range(SIZE):
#     sum += aa[i]
# avg = sum / SIZE
#
# ## 출력
#
# print('영상 평균값 ---> ', avg)
#

import random
SIZE = 10
## 메모리 확보 개념(타 언어 스타일) ##
aa = [] #빈 리스트 준비


for i in range(SIZE):
    aa.append(0)

## 메모리에 필요한 값 대입 ---> 파일 읽기

for i in range(SIZE):
    num = random.randint(0,99)
    aa[i] = num
print('원 영상 ===>', aa)

## 메모리 처리/조작/연산  ---> 알고리즘(컴퓨터 비전, 영상처리)
sum = 0

for i in range(SIZE):
    aa[i] += 10
    if aa[i] > 99 :
        aa[i] = 99


## 출력

print('결과 영상 === > ', aa)
