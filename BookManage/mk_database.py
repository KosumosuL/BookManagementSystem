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
cur.execute('''insert into user values("9161010F0233","赵亮","12345678", "18260071012")''')

cur.execute('''insert into user values("9161010E0233","林零零","12sdsf456", "18261071012")''')
cur.execute('''insert into user values("9161010F0234","蒙萌萌","123456xc", "18260271012")''')
cur.execute('''insert into user values("9161010F0235","能能能","123s456", "18260031012")''')
cur.execute('''insert into user values("9161010F0133","哦哦哦","1233re456", "18264071012")''')
cur.execute('''insert into user values("9161010F0433","七七七","34123456", "18260071112")''')
cur.execute('''insert into user values("916106840842","钱多多","q123456", "13512345678")''')
cur.execute('''insert into user values("916106840843","孙大圣","s123456", "13522345678")''')
cur.execute('''insert into user values("916106840841","李不清","l123456", "13532345678")''')
cur.execute('''insert into user values("916106840844","周山歌","z123456", "13542345678")''')
cur.execute('''insert into user values("916106840845","吴亦水","w123456", "13552345678")''')

cur.execute('''insert into user values("916101","赵阳","10578zy", "15751823678")''')
cur.execute('''insert into user values("916102","周芸","26786zy", "13770995996")''')
cur.execute('''insert into user values("916103","吕亚宁","yn37648", "15952061717")''')
cur.execute('''insert into user values("916104","孟子涵","zh47782", "18625176171")''')
cur.execute('''insert into user values("916105","蔡斌","8764346", "13952078771")''')
cur.execute('''insert into user values("916106","马玉清","myq234234", "15077888771")''')
cur.execute('''insert into user values("916107","穆文浩","732382mwh", "18795969995")''')
cur.execute('''insert into user values("916108","秦淼","7382399", "13913372121")''')

# table book
cur.execute('''create table book
(
    ISBN TEXT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT NOT NULL,
    address TEXT NOT NULL,
    count INTEGER NOT NULL
)
''')

cur.execute('''insert into book values("978-7-302-38141-9","编译原理","王生原、董渊","计算机","501室",5)''')

cur.execute('''insert into book values("978-7-115-40917-1","网络安全理论与应用","俞研、付安民、魏松杰","计算机","403室",3)''')
cur.execute('''insert into book values("978-7-111-32164-4","编译器设计之路","裘巍","计算机","503室",2)''')
cur.execute('''insert into book values("978-7-5051-1785-3","毛泽东独立人格","刘俊坤","文学","201室",2)''')
cur.execute('''insert into book values("7-03-016981-6","图解电路","韦琳","电路","503室",4)''')
cur.execute('''insert into book values("7-309-03879-7","民法学","王利明","法律","301室",2)''')
cur.execute('''insert into book values("978-7-5603-5894-9","高数选讲","刘弘泉","数学","503室",3)''')
cur.execute('''insert into book values("978-7-5517-1493-8","高数笔谈","谢绪恺","数学","503室",2)''')
cur.execute('''insert into book values("7-113-03091-2","线性代数","韩流冰、叶建军、何瑞文","数学","302室",3)''')

cur.execute('''insert into book values("978-7-121-20419-7","算法设计与分析","吴伟昶、方世昌","计算机","402室",5)''')
cur.execute('''insert into book values("978-7-04-023601-9","高等数学","应用数学系","数学","201室",1)''')
cur.execute('''insert into book values("978-7-111-24733-3","数据库基础","斯坦福大学","计算机","402室",2)''')
cur.execute('''insert into book values("978-7-118-09482-4","计算机导论","王操之","计算机","402室",5)''')
cur.execute('''insert into book values("978-7-111-45378-9","计算机网络","张清歌","计算机","402室",6)''')

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

cur.execute('''insert into switch values(111111,"978-7-302-38141-9","9161010F0233","2019-01-01","2019-03-01","2019-02-01")''')

cur.execute('''insert into switch values(111112,"978-7-121-20419-7","916106840842","2019-02-24","2019-04-24","2019-03-10")''')
cur.execute('''insert into switch values(111113,"978-7-04-023601-9","916106840843","2019-02-25","2019-04-25","2019-03-26")''')
cur.execute('''insert into switch values(111311,"978-7-111-24733-3","916106840841","2019-02-24","2019-04-24","2019-03-28")''')
cur.execute('''insert into switch values(111411,"978-7-118-09482-4","916106840844","2019-02-25","2019-04-25","2019-03-06")''')
cur.execute('''insert into switch values(121111,"978-7-111-45378-9","916106840845","2019-02-25","2019-04-25","2019-04-10")''')

cur.execute('''insert into switch values(990001,"978-7-115-40917-1","916101","2019-01-23","2019-03-23","")''')
cur.execute('''insert into switch values(990002,"978-7-115-40917-1","916102","2019-01-24","2019-03-24","")''')
cur.execute('''insert into switch values(990003,"7-309-03879-7","916101","2019-02-02","2019-04-02","")''')
cur.execute('''insert into switch values(990004,"7-113-03091-2","916103","2019-02-03","2019-04-03","")''')
cur.execute('''insert into switch values(990005,"978-7-111-32164-4","916104","2019-02-15","2019-04-15","")''')
cur.execute('''insert into switch values(990006,"978-7-5051-1785-3","916105","2019-03-12","2019-05-12","")''')
cur.execute('''insert into switch values(990007,"7-113-03091-2","916106","2019-03-13","2019-05-13","")''')

cur.execute('''insert into switch values(112311,"978-7-302-38141-9","916106840841","2018-01-01","2018-03-01","2018-02-01")''')
cur.execute('''insert into switch values(611111,"978-7-302-38141-9","916103","2018-05-01","2018-07-01","")''')
cur.execute('''insert into switch values(711111,"978-7-302-38141-9","916106","2019-01-01","2019-03-01","2019-03-01")''')

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