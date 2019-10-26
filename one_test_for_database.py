import mysql.connector
import time

class SQLconnector():
    def __init__(self):
        self._init_list={
            'mul_select_num':5
        }
        self.DataBaseConfig = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': 'deng13508108659',
            'port': 3306,
            'database':'test',
            'charset': 'utf8'
        }
    def _new_connector(self):#生成连接器
        try:
            self.connector = mysql.connector.connect(**self.DataBaseConfig)
            self.connector_cursor = self.connector.cursor()
        except:
            print('connect fails!') #for test
    def run(self,sqlstr):#执行sql语句 并且关闭数据库  返回结果
        self.sqlstr=sqlstr
        if self.sqlstr=='':
            print("run stop because of string is not input")
            return [['']]   #嵌套空串 支持二阶索引
        else:
            self._new_connector()
            try:
                self.connector_cursor.execute(self.sqlstr)
                result = self.connector_cursor.fetchall()
            except mysql.connector.Error as e:
                print('connect fails!{}'.format(e))
                result = [['']]
            finally:
                self.connector.commit()
                self._close()
            if result == []:
                return [['']]
            else:
                return result
    def insert(self,sqlstr):#插入数据函数
        self.sqlstr=sqlstr
        if self.sqlstr=='':
            print("run stop because of string is not input")
            return []
        else:
            self._new_connector()
            try:
                self.connector_cursor.execute(self.sqlstr)
            except mysql.connector.Error as e:
                print('connect fails!{}'.format(e))
            finally:
                self.connector.commit()
                self._close()
    def _close(self):
        self.connector_cursor.close()
        self.connector.close()
dbc=SQLconnector()
id=5
str='小橘子'
k="select id from things_inf where description like '%" + str + "%' or title like '%" + str + "%'"
print(k)