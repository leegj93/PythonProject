import operator

ttL= [('토마스',5), ('헨리', 8), ('에드워드', 9), ('토마스', 12), ('에드워드', 1) ]

tD={}
tL=[]
tR, cR= 1, 1

for tmpTup in ttL :
    tName = tmpTup[0]
    tWeight = tmpTup[1]
    if tName in tD :
        tD[tName] += tWeight
    else:
        tD[tName] = tWeight
print(list(tD.items()))

tL=sorted(tD.items(),key= operator.itemgetter(1), reverse =True)

print(tL)
