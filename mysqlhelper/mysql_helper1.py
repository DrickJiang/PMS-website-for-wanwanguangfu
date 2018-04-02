# coding: utf8
import pymysql

class Mysql_helper():
    def __init__(self, host, user,password,db,port,charset ='utf-8'):
        self.conn = pymysql.connect(host=host,
                                    user=user,
                                    password=password,
                                    db=db,
                                    port=port,
                                    charset=charset)
        self.cursor = self.conn.cursor()


    #关闭数据库连接
    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    #执行sql语句不返回结果
    def execute_sql(self,sql,params = None):
        try:
            self.cursor.execute(sql,params)
            self.conn.commit()
            self.close_connection()
        except Exception as e:
            print(e)

    #执行sql语句返回结果，根据是否需要选择查询一项或多项
    def query_sql(self,sql,params=None,one=True):
        try:
            self.cursor.execute(sql, params)
            result = self.cursor.fetchall()
            self.close_connection()
            return (result[0] if result else None) if one else result
        except Exception as e:
            print(e)


