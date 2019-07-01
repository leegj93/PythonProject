inFp = open('c:/windows/win.ini', 'rt')
outFp = open('c:/images/new_win.ini','w')
while True:
    inStr = inFp.readline()
    if not inStr:
        break
    outFp.writelines(inStr)

#
# inStrList =inFp.readlines()
# print(inStrList)
# for line in inStrList :
#     print(line, end='')

inFp.close()
outFp.close()
print('OK~')