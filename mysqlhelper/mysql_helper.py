# coding: utf8
import pymysql
# from flask import g

# database_url = 'host="10.0.0.12",user="root",password="123456",db="mar",port=3306'

class Mysql_helper():
    def __init__(self, host, user, password,db,port, charset='utf8', cursorclass= pymysql.cursors.DictCursor):
        self.conn = pymysql.connect(host=host,
                                    user=user,
                                    password=password,
                                    db=db,
                                    port=port,
                                    charset=charset,
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    #用g建立数据库连接,包括使用app生命周期来处理关闭数据库连接，等后期更熟悉flask源码后处理实现
        """
    def get_db(self):
        db = getattr(g,'_database',None)
        if db is None:
            db = g._database = pymysql.connect(database_url)
        return db
        """

    #建立/打开数据库连接，因为封装读取之后出现中文字符不识别的问题，所以将连接和路由放置在init中，本处注释
    """
    def open_db(self):
        self.conn = pymysql.connect(self.host,self.user,self.password,self.db,self.port,self.charset)
        self.cursor = self.conn.cursor()
    """

    #关闭数据库连接
    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    #执行sql语句不返回结果
    def execute_sql(self, sql, params=()):
        try:
            self.cursor.execute(sql, params)
            self.conn.commit()
            # self.close_connection()
        except Exception as e:
            print(e)

    #执行sql语句返回结果，根据是否需要选择查询一项或多项
    def query_sql(self, sql, params=(), one=True):
        try:
            self.cursor.execute(sql,params)
            result = self.cursor.fetchall()
            # self.close_connection()
            return (result[0] if result else None) if one else result
        except Exception as e:
            print(e)





