import sqlite3 as sql

conn = sql.connect("test.db")
cur = conn.cursor()

# table user
cur.execute('''create table user
(
    ID TEXT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    phonenum TEXT NOT NULL
)
''')

cur.execute('''insert into user
values(
"9161010F0233", 
"lucaszhao",
"123456", 
"18260071012"
)
''')

# table book
cur.execute('''create table book
(
    ISBN TEXT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    address TEXT NOT NULL,
    count INTEGER NOT NULL
)
''')

cur.execute('''insert into book
values(
"978-7-302-38141-9", 
"编译原理",
"计算机", 
"501室",
5
)
''')

# table switch
cur.execute('''create table switch
(
    SID INTEGER PRIMARY KEY NOT NULL,
    ISBN TEXT NOT NULL,
    ID TEXT NOT NULL,
    BORROWTIME TEXT NOT NULL,
    SRETURNTIME TEXT NOT NULL,
    RETURNTIME TEXT
)
''')

cur.execute('''insert into switch
values(
111111, 
"978-7-302-38141-9",
"9161010F0233", 
"20190101",
"20190301",
"20190201"
)
''')

conn.commit()

cur.execute('select * from user')
conn.text_factory = str
print(cur.fetchall())

cur.execute('select * from book')
conn.text_factory = str
print(cur.fetchall())

cur.execute('select * from switch')
conn.text_factory = str
print(cur.fetchall())

cur.close()
conn.close()