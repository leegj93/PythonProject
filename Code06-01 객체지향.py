class Car:
    #자동차 속성
    color = None
    speed = 0
    # 자동차의 행위(==> 함수, 기능)
    # 메소드
    def upSpeed(self, value):
        self.speed += value
    def downSpeed(self, value):
        self.speed -= value


########################
myvalue = 0
car1 = Car(); car2=Car()

car1.color = "빨강"
car1.speed = 50
car1.upSpeed(100)

print(car1.speed)