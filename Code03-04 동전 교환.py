## 함수 선언부 ##



## 변수 선언부 ##
money, c500, c100, c50, c10 =[0] * 5 # 돈, 동전 500, 100....

##메인 코드부 ##

if __name__ == '__main__' :
    money = int(input('바꿀 돈 : '))
    c500 = money // 500; money %= 500
    c100 = money // 100; money %= 100
    c50 = money // 50; money %= 50
    c10 = money // 10; money %= 10

    print('500원: ', c500, '100원: ', c100, '50원: ', c50, ' 10원', c10,  '나머지:', money)

