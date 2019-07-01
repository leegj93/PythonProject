def func1() :
    global a
    a = 10
    print('func1 ---> ', a)


def func2() :
    print('func2 ---> ', a)


def cal(v1, v2) :
    result1 = v1 + v2
    result2 = v1 - v2
    return result1, result2

# 변수 선언부

a = 1234

func1()
func2()