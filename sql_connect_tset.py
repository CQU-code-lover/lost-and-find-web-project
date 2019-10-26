#sql_connect_test
import mysql.connector
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

    def _new_connector(self):  # 生成连接器
        try:
            self.connector = mysql.connector.connect(**self.DataBaseConfig)
            self.connector_cursor = self.connector.cursor()
        except:
            print('connect fails!')  # for test

    def run(self, sqlstr):  # 执行sql语句 并且关闭数据库  返回结果
        self.sqlstr = sqlstr
        if self.sqlstr=='':
            print("run stop because of string is not input")
            return {}
        else:
            self._new_connector()
            try:
                self.connector_cursor.execute(self.sqlstr)
            except mysql.connector.Error as e:
                print('connect fails!{}'.format(e))
            result = self.connector_cursor.fetchall()
            self.connector.commit()
            self.connector_cursor.close()
            self.connector.close()
            return result

    def close(self):
        self.connector_cursor.close()
        self.connector.close()
dbc=SQLconnector()

