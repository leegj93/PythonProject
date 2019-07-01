import sqlite3

conn = sqlite3.connect("samsongDB")# 1. DB connecting
cur = conn.cursor() # 2. create cursor(connected rope)


sql = "CREATE TABLE IF NOT EXISTS userTable(userID INT, userName char(5))"
cur.execute(sql)


sql= "INSERT INTO userTable VALUES(1, '홍길동')";
cur.execute(sql)
sql= "INSERT INTO userTable VALUES(2, '이순신')";
cur.execute(sql)

cur.close()
conn.commit()
conn.close() # 6. DB disconnect

print('OK')
