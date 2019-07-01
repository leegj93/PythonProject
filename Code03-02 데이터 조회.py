import sqlite3

conn = sqlite3.connect("samsongDB")# 1. DB connecting
cur = conn.cursor() # 2. create cursor(connected rope)
sql ="SELECT * FROM userTable"
cur.execute(sql)

rows= cur.fetchall()
print(rows)

cur.close()

conn.close() # 6. DB disconnect

print('OK')
