# PMS-website-for-wanwanguangfu
江苏弯弯光伏科技有限公司。written by Flask, in python3 environment.
实现功能：
1.在后台管理页面实现灯具的图片、分类与特征参数的CRUD操作；
2.后台管理员的登录与退出功能，密码进行哈希加密；
3.前台实现对产品的特征与分类搜索;
4.只使用SQL语句封装，未使用ORM/WTForm框架。


# Apr 2nd 
First commit:

database server: Mysql;
database name:mar;
database table : admin/category1/productinfo1.

sql statement:
    create table useinfo (
    id int auto_increment primary key not null,
    usename varchar(20) not null,
    email varchar(50) not null,
    phonenumber varchar(20) not null,
    password char(40) ,
    gender bit default 1,
    birthdate datetime
    );

CREATE TABLE category1 (
  id INT AUTO_INCREMENT PRIMARY KEY NOT NULL ,
  categoryname VARCHAR(40),
  explanation VARCHAR(40)
);


INSERT INTO category1(categoryname,explanation) VALUES ('路灯','用途'),('高杆灯','用途'),('景观灯','用途'),
  ('球场灯','用途'),('投光灯','用途'),('工矿灯','用途'),('日光灯','用途'),('球泡灯','用途'),('格栅灯','用途');

INSERT INTO category1(id,categoryname,explanation) VALUES (20,'太阳能','动力能源'),(21,'风能','动力能源'),
  (22,'电网电力','动力能源'),(23,'混合动力','动力能源');

INSERT INTO category1(id,categoryname,explanation) VALUES (30,'LED模组','光源材料'),(31,'LED颗粒','光源材料'),
  (32,'LED COB','光源材料'),(33,'金卤灯','光源材料'),(34,'高压钠灯','光源材料'),(35,'无极灯','光源材料'),
  (36,'节能灯','光源材料');

INSERT INTO category1(id,categoryname,explanation) VALUES (70,'现代','外形风格'),(71,'传统','外形风格'),
  (72,'古典','外形风格'),(73,'经典','外形风格'),(74,'时尚','外形风格');

INSERT INTO category1(id,categoryname,explanation) VALUES (90,'花灯','主题'),(91,'壁灯','主题'),(92,'爱国','主题');

INSERT INTO category1(id,categoryname,explanation) VALUES (120,'欧普','品牌'),(121,'博世','品牌');

CREATE TABLE productinfo1 (
  id INT AUTO_INCREMENT PRIMARY KEY NOT NULL ,
  xinghao VARCHAR(40) NOT NULL ,
  tupian VARCHAR(60),
  yongtu INT,
  dongli INT,
  cailiao INT,
  fengge INT,
  zhuti INT,
  pinpai INT,
  danjia INT,
  gonglv VARCHAR(20),
  gtl VARCHAR(20),
  sewen VARCHAR(20),
  fgjd VARCHAR(20),
  xszs VARCHAR(20),
  zbq VARCHAR(20),
  FOREIGN KEY(yongtu) REFERENCES category1(id),
  FOREIGN KEY(dongli) REFERENCES category1(id),
  FOREIGN KEY(cailiao) REFERENCES category1(id),
  FOREIGN KEY(fengge) REFERENCES category1(id),
  FOREIGN KEY(zhuti) REFERENCES category1(id),
  FOREIGN KEY(pinpai) REFERENCES category1(id)
);

INSERT INTO productinfo1 VALUES (3,'suzhou20180310',NULL ,2,21,33,71,90,121,70,8,'100','40001','45','70','三个月');

SELECT p.*,
  c.categoryname FROM productinfo1 AS p
INNER JOIN category1 as c ON p.yongtu = c.id ;

select
p.id pid,p.xinghao,p.tupian,p.danjia,p.gonglv,p.gtl,p.sewen,p.fgjd,p.xszs,p.zbq,
a.categoryname AS 功能,
b.categoryname AS 动力,
c.categoryname AS 材料,
d.categoryname AS 风格,
e.categoryname AS 主题,
f.categoryname AS 品牌
from productinfo1 p
left join category1 a on a.id = p.yongtu
left join category1 b on b.id = p.dongli
left join category1 c on c.id = p.cailiao
left join category1 d on d.id = p.fengge
LEFT JOIN category1 e on e.id = p.zhuti
LEFT JOIN category1 f on f.id = p.pinpai;

select
p.id pid,p.xinghao,p.tupian,p.danjia,p.gonglv,p.gtl,p.sewen,p.fgjd,p.xszs,p.zbq,
a.categoryname AS 功能,b.categoryname 动力
  from productinfo1 p
INNER join category1 a on a.id = p.yongtu
INNER JOIN category1 b on b.id = p.dongli;

DELETE FROM productinfo1 WHERE id =6;
INSERT INTO productinfo1(xinghao) VALUES ('sjs3')


INSERT INTO category1 VALUES (119,'其他','品牌');

alter table productinfo1 add shuoming TEXT;

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

update productinfo1 set xszs= '95' WHERE xinghao = '323'

SELECT * FROM productinfo1 WHERE xinghao like '%sh%';
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
                    WHERE p.id> 0 and p.xinghao like '%sh%';

create table admin(
id int auto_increment primary key not null,
name varchar(40) unique key not null,
pwd char(40) unique key not null);

insert into admin values(0,'hugangwan','7c4a8d09ca3762af61e59520943dc26494f8941b');
