from flask import Flask,render_template,request,redirect,url_for,send_from_directory,flash,session
from mysqlhelper.mysql_helper import Mysql_helper
import os
from datetime import datetime
from hashlib import sha1

app = Flask(__name__)
app.secret_key = "askhiudh23#$^3*rt&%@74"

UPLOAD_FOLODER = r'.\uploads'
ALLOWED_EXTENSIONS = ['.jpg','.png','.gif']

#检查文件上传格式是否允许
def check_pic_ext(tupian):
    _,ext = os.path.splitext(tupian)
    return ext.lower() in ALLOWED_EXTENSIONS

# 呈现特定目录（此处是Uploads）下的文件,加上app route的装饰器为了能被后端直接调用
@app.route('/profile/<filename>/')
def render_file(filename):
    return send_from_directory(UPLOAD_FOLODER,filename)

@app.route('/')
def index():
    return render_template('base1.html')

#展示管理员可添加产品数据页面
@app.route('/admin/product_add/')
def product_add():
    if session.get('admin',None) is None:
        return redirect(url_for('admin_login'))
    else:
        db = Mysql_helper("10.0.0.12","root","123456","mar",3306)
    #得到页面下拉列表所需数据
        yongtus = db.query_sql("select id,categoryname from category1 WHERE explanation = '用途'", one=False)
        donglis = db.query_sql("select id,categoryname from category1 WHERE explanation = '动力能源'", one=False)
        cailiaos = db.query_sql("select id,categoryname from category1 WHERE explanation = '光源材料'", one=False)
        fengges = db.query_sql("select id,categoryname from category1 WHERE explanation = '外形风格'", one=False)
        zhutis = db.query_sql("select id,categoryname from category1 WHERE explanation = '主题'", one=False)
        pinpais = db.query_sql("select id,categoryname from category1 WHERE explanation = '品牌'", one=False)
        db.close_connection()
        return render_template('product_add.html',yongtus = yongtus,donglis=donglis,cailiaos= cailiaos,fengges=fengges,zhutis=zhutis,pinpais=pinpais)

#新增产品数据之后提交
@app.route('/admin/post_add_product/',methods=['POST'])
def post_add_product():
    if request.method == 'POST':
        #从request的form中获取
        xinghao = request.form.get('xinghao','')
        yongtu = request.form.get('yongtu',1)
        dongli = request.form.get('dongli',20)
        cailiao = request.form.get('cailiao',30)
        fengge = request.form.get('fengge',70)
        zhuti = request.form.get('zhuti',90)
        pinpai = request.form.get('pinpai',119)
        danjia = request.form.get('danjia','')
        gonglv = request.form.get('gonglv', '')
        gtl = request.form.get('gtl', '')
        sewen = request.form.get('sewen', '')
        fgjd = request.form.get('fgjd', '')
        xszs = request.form.get('xszs', '')
        zbq = request.form.get('zbq', '')
        shuoming = request.form.get('shuoming','')
        tupian = None
        #判断图片是否存在，是否符合格式要求（注意一定是判断文件的filename而非文件本身），ok的话，设置文件新名并以此名保存上传
        if request.files.get('tupian',None):
            pic = request.files.get('tupian')
            if check_pic_ext(pic.filename):
                img_path1 = datetime.now().strftime("%Y%m%d%H%M%f") + os.path.splitext(pic.filename)[1]
                pic.save(os.path.join(UPLOAD_FOLODER,img_path1))

        db = Mysql_helper("10.0.0.12", "root", "123456", "mar", 3306)

        sql = "insert into productinfo1( xinghao, tupian, yongtu, dongli, cailiao, fengge, zhuti, pinpai, danjia, gonglv, gtl, sewen, fgjd, xszs, zbq, shuoming) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (xinghao, img_path1, yongtu, dongli, cailiao, fengge, zhuti, pinpai, danjia, gonglv, gtl, sewen, fgjd, xszs, zbq, shuoming)

        db.execute_sql(sql,params)
        db.close_connection()
        return redirect(url_for('product_add'))

@app.route('/admin/product_list/')
def p():
    if session.get('admin',None) is None:
        return redirect(url_for('admin_login'))
    else:
        return redirect('/admin/product_list/1/')

#显示所有产品列表
@app.route('/admin/product_list/<id>/')
def product_list(id =1):
    if session.get('admin',None) is None:
        return redirect(url_for('admin_login'))
    else:
        db = Mysql_helper("10.0.0.12","root","123456","mar",3306)

        sql = """
    select p.xinghao,
    a.categoryname AS yongtu,
    b.categoryname AS dongli,
    c.categoryname AS cailiao,
    d.categoryname AS fengge,
    e.categoryname AS zhuti,
    f.categoryname AS pinpai,
    p.danjia from productinfo1 p
    LEFT JOIN category1 a ON a.id = p.yongtu
    LEFT JOIN category1 b ON b.id = p.dongli
    LEFT JOIN category1 c ON c.id = p.cailiao
    LEFT JOIN category1 d ON d.id = p.fengge
    LEFT JOIN category1 e ON e.id = p.zhuti
    LEFT JOIN category1 f ON f.id = p.pinpai
    """
        products = db.query_sql(sql, one=False)
        #计算总数，以用于分页
        sql2 = "select count(*) from productinfo1"
        pro_number= db.query_sql(sql2)
        db.close_connection()
        unit_products =[]
        #i是用来显示序号的，mysql内不存在rowid，id不连续，显示出来会比较难看。使用如下代码自定义id能显得好看
        for i,product in enumerate(products[10*(int(id)-1):(10*int(id))]):
            unit_products.append(((i+10*int(id)-9),product))
        #总页数
        pages = ((pro_number['count(*)'])//10 +1)
        return render_template('product_list.html', products = unit_products,pages= pages,id = int(id))

#显示单个产品的具体信息
@app.route('/admin/product_info/<xinghao>')
def product_info(xinghao = None):
    if session.get('admin',None) is None:
        return redirect(url_for('admin_login'))
    else:
        db = Mysql_helper("10.0.0.12", "root", "123456", "mar", 3306)
        sql = """
    select p.*,
    a.categoryname AS yongtu,
    b.categoryname AS dongli,
    c.categoryname AS cailiao,
    d.categoryname AS fengge,
    e.categoryname AS zhuti,
    f.categoryname AS pinpai from productinfo1 p
    LEFT JOIN category1 a ON a.id = p.yongtu
    LEFT JOIN category1 b ON b.id = p.dongli
    LEFT JOIN category1 c ON c.id = p.cailiao
    LEFT JOIN category1 d ON d.id = p.fengge
    LEFT JOIN category1 e ON e.id = p.zhuti
    LEFT JOIN category1 f ON f.id = p.pinpai
    WHERE p.xinghao = %s"""
        params = xinghao
        product = db.query_sql(sql,params,one=True)
        db.close_connection()
        return render_template('product_info.html',product = product)

#删除某项
@app.route('/admin/product_list/del/<xinghao>')
def product_del(xinghao = None):
    if xinghao:
        db = Mysql_helper("10.0.0.12", "root", "123456", "mar", 3306)
        sql = 'delete from productinfo1 WHERE xinghao = %s'
        db.execute_sql(sql,params=(xinghao,))
        db.close_connection()
    return redirect(url_for('p'))

#编辑产品信息，找到数据库信息并显示
@app.route('/admin/product_edit/<xinghao>')
def product_edit(xinghao = None):
    if session.get('admin',None) is None:
        return redirect(url_for('admin_login'))
    else:
        db = Mysql_helper("10.0.0.12", "root", "123456", "mar", 3306)
        yongtus = db.query_sql("select id,categoryname from category1 WHERE explanation = '用途'", one=False)
        donglis = db.query_sql("select id,categoryname from category1 WHERE explanation = '动力能源'", one=False)
        cailiaos = db.query_sql("select id,categoryname from category1 WHERE explanation = '光源材料'", one=False)
        fengges = db.query_sql("select id,categoryname from category1 WHERE explanation = '外形风格'", one=False)
        zhutis = db.query_sql("select id,categoryname from category1 WHERE explanation = '主题'", one=False)
        pinpais = db.query_sql("select id,categoryname from category1 WHERE explanation = '品牌'", one=False)

        sql = """
    select p.xinghao,p.tupian,p.danjia,p.gonglv,p.gtl,p.sewen,p.fgjd,p.xszs,p.zbq,p.shuoming,
    p.yongtu AS yongtuid,p.dongli AS dongliid,p.cailiao AS cailiaoid,p.fengge AS fenggeid,
    p.pinpai AS pinpaiid,p.zhuti AS zhutiid,
    a.categoryname AS yongtu,
    b.categoryname AS dongli,
    c.categoryname AS cailiao,
    d.categoryname AS fengge,
    e.categoryname AS zhuti,
    f.categoryname AS pinpai from productinfo1 p
    LEFT JOIN category1 a ON a.id = p.yongtu
    LEFT JOIN category1 b ON b.id = p.dongli
    LEFT JOIN category1 c ON c.id = p.cailiao
    LEFT JOIN category1 d ON d.id = p.fengge
    LEFT JOIN category1 e ON e.id = p.zhuti
    LEFT JOIN category1 f ON f.id = p.pinpai
    WHERE p.xinghao = %s
    """
        params = xinghao
        product = db.query_sql(sql, params, one=True)
        db.close_connection()

        return render_template('product_edit.html',product = product,yongtus=yongtus,donglis = donglis,cailiaos=cailiaos,fengges=fengges,zhutis=zhutis,pinpais=pinpais)

#保存编辑好的信息提交到数据库
@app.route('/admin/save_edit/',methods=['POST'])
def save_edit_product():
    if request.method == 'POST':
        xinghao = request.form.get('xinghao', '')
        yongtu = request.form.get('yongtu', 1)
        dongli = request.form.get('dongli', 20)
        cailiao = request.form.get('cailiao', 30)
        fengge = request.form.get('fengge', 70)
        zhuti = request.form.get('zhuti', 90)
        pinpai = request.form.get('pinpai', 119)
        danjia = request.form.get('danjia', '')
        gonglv = request.form.get('gonglv', '')
        gtl = request.form.get('gtl', '')
        sewen = request.form.get('sewen', '')
        fgjd = request.form.get('fgjd', '')
        xszs = request.form.get('xszs', '')
        zbq = request.form.get('zbq', '')
        shuoming = request.form.get('shuoming', '')
        #
        # a = [xinghao,yongtu,dongli,cailiao,fengge,zhuti,pinpai,danjia,gonglv,gtl,sewen,fgjd,xszs,zbq,shuoming]
        # print(a)

        db = Mysql_helper("10.0.0.12", "root", "123456", "mar", 3306)
        sql = """
        update productinfo1 set
        yongtu=%s,dongli=%s,cailiao=%s,fengge=%s,zhuti=%s,pinpai=%s,danjia=%s,gonglv=%s,gtl=%s,sewen=%s,fgjd=%s,xszs=%s, zbq=%s,shuoming=%s
         where xinghao = %s
        """
        db.execute_sql(sql,(yongtu,dongli,cailiao,fengge,zhuti,pinpai,danjia,gonglv,gtl,sewen,fgjd,xszs,zbq,shuoming,xinghao))
        db.close_connection()
        flash('用户更新成功！')

    return redirect(url_for('p'))

#客户检索产品页面，这里有个bug：如果用户在第二页、第三页搜索则在目标数据量不足时无搜索记录
@app.route('/search_product/<id>')
def search_product(id=1):
    db = Mysql_helper("10.0.0.12", "root", "123456", "mar", 3306)
    # 给用途、品牌的下拉列表以数据库内选项
    yongtus = db.query_sql("select id,categoryname from category1 WHERE explanation = '用途'", one=False)
    pinpais = db.query_sql("select id,categoryname from category1 WHERE explanation = '品牌'", one=False)

    if request.args.get('yongtu',None) is None:
        sql = r"""
            select p.xinghao,
            a.categoryname AS yongtu,
            b.categoryname AS dongli,
            c.categoryname AS cailiao,
            d.categoryname AS fengge,
            e.categoryname AS zhuti,
            f.categoryname AS pinpai,
            p.danjia from productinfo1 p
            LEFT JOIN category1 a ON a.id = p.yongtu
            LEFT JOIN category1 b ON b.id = p.dongli
            LEFT JOIN category1 c ON c.id = p.cailiao
            LEFT JOIN category1 d ON d.id = p.fengge
            LEFT JOIN category1 e ON e.id = p.zhuti
            LEFT JOIN category1 f ON f.id = p.pinpai
            """
        products = db.query_sql(sql, one=False)
    else:
        sql = r"""
                    select p.xinghao,
                    a.categoryname AS yongtu,
                    b.categoryname AS dongli,
                    c.categoryname AS cailiao,
                    d.categoryname AS fengge,
                    e.categoryname AS zhuti,
                    f.categoryname AS pinpai,
                    p.danjia from productinfo1 p
                    LEFT JOIN category1 a ON a.id = p.yongtu
                    LEFT JOIN category1 b ON b.id = p.dongli
                    LEFT JOIN category1 c ON c.id = p.cailiao
                    LEFT JOIN category1 d ON d.id = p.fengge
                    LEFT JOIN category1 e ON e.id = p.zhuti
                    LEFT JOIN category1 f ON f.id = p.pinpai
                    WHERE p.id> 0 """
        yongtu = request.args.get('yongtu', None)
        pinpai = request.args.get('pinpai', None)
        xinghao = request.args.get('xinghao', '')
        print('品牌是--{}'.format(pinpai))
        jiagequjian = request.args.get('danjia', None)
        dict1 = {'a': 'and p.danjia <= 20 ', 'b': 'and p.danjia > 20 & p.danjia <= 100 ', 'c': 'and p.danjia > 100 & p.danjia <= 1000 ',
             'd': 'and p.danjia >1000 ','e':''}
        yongtu_sql = "and p.yongtu = {} ".format(yongtu) if yongtu != '---' else ''
        pinpai_sql = "and p.pinpai = {} ".format(pinpai) if pinpai != '---' else ''
        #双%是转义需要
        xinghao_sql = "and p.xinghao like '%%{}%%'".format(xinghao) if xinghao != '' else ''
        sql1 = sql + yongtu_sql + pinpai_sql + dict1.get(jiagequjian) + xinghao_sql
        products = db.query_sql(sql1,  one=False)
    db.close_connection()
    unit_products =[]
    #i是用来显示产品序号的，mysql内不存在rowid，自定义id不连续，显示出来比较难看。
    if products:
        for i,product in enumerate(products[10*(int(id)-1):(10*int(id))]):
            unit_products.append(((i+10*int(id)-9),product))
    else:
        unit_products = []
    #总页数
    pages = (len(products) // 10 + 1)
    return render_template('search_product.html', products = unit_products,pages= pages,id = int(id),yongtus=yongtus,pinpais=pinpais)

@app.route('/search_product/')
def s():
    return redirect('/search_product/1')

#登录页面
@app.route('/login/',methods=['POST','GET'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        pwd = request.form.get('pwd')
        s1 = sha1()
        s1.update(pwd.encode("utf8"))
        pwd_hash = s1.hexdigest()
        sql = 'select count(*) as Count from admin WHERE NAME =%s and pwd =%s'
        db = Mysql_helper("10.0.0.12", "root", "123456", "mar", 3306)
        result = db.query_sql(sql,(username,pwd_hash),one=True)
        if int(result.get('Count')) > 0:
            session['admin'] = username
            return redirect(url_for('p'))
        else:
            flash('用户名或密码错误')
    return render_template('admin_login.html')

# 退出登录
@app.route('/logout/')
def logout():
    session.pop('admin')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
