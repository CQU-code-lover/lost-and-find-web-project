import mysql.connector

# mysql1.py
config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',
    'port': 3306,
    'database': 'test',
    'charset': 'utf8'
}
try:
    cnn = mysql.connector.connect(**config)
except mysql.connector.Error as e:
    print('connect fails!{}'.format(e))
cursor = cnn.cursor()
try:
    sql_query = 'select name,age from stu ;'
    cursor.execute(sql_query)
    for name, age in cursor:
        print (name, age)
except mysql.connector.Error as e:
    print('query error!{}'.format(e))
finally:
    cursor.close()
    cnn.close()



#批量插入

def select2(sql_cmd, param):
    """
    :param sql_cmd sql 命令
    :param param 参数
    """
    try:
        conn = mysql.connector.connect(**config)
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))

    cursor = conn.cursor()
    try:
        cursor.execute(sql_cmd, param)
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))
    finally:
        cursor.close()
        conn.close()

if __name__ ==  '__main__':
    sql_cmd = "insert into stu (name, age, sex) value (%s, %s, %s)"
    param = ('yangguo', 28, 'male')
    select2(sql_cmd=sql_cmd, param=param)    # 将命令和参数分隔开，操作起来更加安全

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123456",
    database="runoob_db"
)
mycursor = mydb.cursor()

sql = "INSERT INTO sites (name, url) VALUES (%s, %s)"
val = [
    ('Google', 'https://www.google.com'),
    ('Github', 'https://www.github.com'),
    ('Taobao', 'https://www.taobao.com'),
    ('stackoverflow', 'https://www.stackoverflow.com/')
]

mycursor.executemany(sql, val)

mydb.commit()  # 数据表内容有更新，必须使用到该语句

print(mycursor.rowcount, "记录插入成功。")
#!/usr/bin/env python
# encoding: utf-8



#自定义异常类
class IllegalException(Exception):
    '''
    Custom exception types
    '''
    def __init__(self, parameter, para_value):
        err = 'The parameter "{0}" is not legal:{1}'.format(parameter, para_value)
        Exception.__init__(self, err)
        self.parameter = parameter
        self.para_value = para_value
#使用异常   可以传入参数
#raise (IllegalException(integer[0], integer[1]))