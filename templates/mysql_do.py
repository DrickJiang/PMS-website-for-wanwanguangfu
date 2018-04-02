import pymysql
from hashlib import sha1

#打开数据库连接
db= pymysql.connect(host="10.0.0.12",user="root",password="123456",db="mar",port=3306)

#建立游标
c = db.cursor()
#一、一整段参数
"""
#待执行的语句
sql = 'INSERT INTO useinfo VALUES %s'
# sql = 'SELECT * from useinfo'
user = (3,"jackliu","322381121@qq.com","17777777777","40BD001563085FC35165329EA1FF5C5ECBDBBEEF",1,"19900604")

#执行语句
try:
    c.execute(sql,(user,))
    # c.execute(sql)
    # result = c.fetchall()
    # print(result)
    db.commit()
    c.close()
    db.close()
except Exception as e:
    print(e)
# finally:
#     c.close()
#     db.close()
"""


# 二、多参数分开获取
"""
#待执行语句
sql = 'insert into useinfo(usename, email, phonenumber, password, gender, birthdate) VALUES (%s,%s,%s,%s,%s,%s)'
usename = input('请输入您的姓名')
email = input('请输入您的邮箱')
phonenumber = input('请输入您的电话')
# 对用户输入密码进行sha1方式加密
pwd = input('请输入你的密码')
s1 = sha1()
s1.update(pwd.encode("utf-8"))
password = s1.hexdigest()

gender = 0 if input('请输入您的性别') == '女' else 1
birthdate = input('请输入您的出生日期')

try:
    c.execute(sql,[usename,email,phonenumber,password,gender,birthdate])
    db.commit()
    c.close()
    db.close()
except Exception as e:
    print(e)
"""

# 三、测试查询与输出
#待执行语句
sql = "select id,usename,email,phonenumber from useinfo WHERE id >5 ORDER BY id"
#执行语句
try:
    c.execute(sql)
    result = c.fetchall()
    print(result)
    print('第三项是{}'.format(result[2]))
    for r in result:
        print(r)
    c.close()
    db.close()
except Exception as e:
    print(e)

#测试fetchone()和它的游标走向
# try:
#     c.execute(sql)
#     for i in range(0,3):
#         result = c.fetchone()
#         print(result)
#         print(result[2])
# except Exception as e:
#     print(e)

