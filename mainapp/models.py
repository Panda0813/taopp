# 声明数据库表对应的模型类
from datetime import datetime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import backref, relationship

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)  #初始化数据库
    Migrate(app,db)  #初始化数据库迁移命令

class Letter(db.Model):
    __tablename__ = 't_letter'

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(10))

# 用户角色
class Role(db.Model):
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(20))
    rights = Column(Integer,default=1)

# 权限
class Qx(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    right = Column(Integer)


class City(db.Model):
    __tablename__ = 't_city'

    id = Column(Integer,primary_key=True,autoincrement=True)
    parentId = Column(Integer,default=0)
    regionName = Column(String(30))
    cityCode = Column(Integer)
    pinYin = Column(String(50))

    letter_id = Column(Integer,ForeignKey('t_letter.id'))
    letter = relationship('Letter',backref = backref('cities',lazy=True))

class User(db.Model):
    __tablename__ = 't_user'

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(50),unique=True)  #用户名
    passwd = Column(String(50))
    nickname = Column(String(30))  #昵称
    email = Column(String(30),unique=True)
    phone = Column(String(12),unique=True)
    # 是否激活，默认未激活，初次注册要用邮箱激活
    is_active = Column(Boolean,default=False)
    is_live = Column(Boolean,default=True)
    regist_time = Column(DateTime,default=datetime.now())
    last_login_time = Column(DateTime,onupdate=datetime.now())

    # 新增头像的属性
    photo_1 = Column(String(100),nullable=True)  # 大图
    photo_2 = Column(String(100),nullable=True)  # 小图

    # 用户权限(被管理员授权)
    rights = Column(Integer,default=1)

    # 用户角色
    role_id = Column(Integer,ForeignKey('role.id'))
    role = relationship('Role',backref=backref('users',lazy=True))

# 电影信息
class Movies(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer,primary_key=True,autoincrement=True)
    showname = Column(String(100))  #中文名
    shownameen = Column(String(200))  #英文名
    director = Column(String(100))  # 导演
    leadingRole = Column(String(300))  # 主演
    type = Column(String(50))  # 类型
    country = Column(String(100))  #国家
    language = Column(String(50))  #语言
    duration = Column(Integer)  #电影时长
    screeningmodel = Column(String(20))  #放映模式(2D 3D 4D),可以使用枚举
    openday = Column(DateTime)  #上映时间
    backgroundpicture = Column(String(100))  #背景图片
    # flag 0: 所有   1: 热映   2: 即将上映
    flag = Column(Integer)  #状态(热映 即将上映)
    isdelete = Column(Boolean,default=False)  #是否删除,默认未删除


#电影院信息
class Cinemas(db.Model):
    __tablename__ = 'cinemas'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(100))  #影院名
    city = Column(String(50))  #所在城市
    district = Column(String(50))  #区域
    address = Column(String(200))  #地址
    phone = Column(String(20))  #电话
    score = Column(Float)  #评分
    hallnum = Column(Integer)  # 影厅数量
    servicecharge = Column(Float)  #服务费
    astrict = Column(Integer)  #限购数量
    flag = Column(Integer)  # 状态(营业1，休息0)
    isdelete = Column(Boolean,default=False)  # 是否删除




# 影厅信息
# class Halls(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50))
#     screeningtype = Column(Enum(0, 1, 2))  #屏幕类型(0:2D  1:3D  2:4D)
#     video = Column(Enum(0, 1, 2))  #音效(0普通、1环绕、2杜比)
#     sites = Column(Integer)  # 座位数量
#     flag = Column(Integer)  # 状态(关闭0，开放1)
#     isdelete = Column(Boolean, default=False)  # 是否删除
#
#     # 与影院的关系
#     cinemaid = Column(Integer,ForeignKey('cinemas.id'))
#     cinema = relationship('Cinemas',backref=backref('halls',lazy=True))
#
# #影厅排期
# class HallSchedulings:
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     pricetype = Column(Enum(0, 1, 2))  # 价格类型(0原价、1售价、2最低价)
#     marketprice = Column(Float)  #原价
#     price = Column(Float)  #售价
#     opentime = Column(DateTime)  #开始放映时间
#     duration = Column(Integer)  # 时长
#     createtime = Column(DateTime,default=datetime.now())  #创建时间
#     updatetime = Column(DateTime,onupdate=datetime.now())  #最后更新时间
#     flag = Column(Integer)  # 状态(未放映0、正在放映1、结束放映2)
#     is_delete = Column(Boolean,default=False)  #是否删除
#
#     # 与影院的关系
#     cinemaid = Column(Integer, ForeignKey('cinemas.id'))
#     cinema = relationship('Cinemas', backref=backref('hallschedules', lazy=True))
#     # 与影厅的关系
#     hallid = Column(Integer,ForeignKey('halls.id'))
#     hall = relationship('Halls',backref=backref('hallschedules', lazy=True))
#     # 与电影的关系
#     movieid = Column(Integer,ForeignKey('movies.id'))
#     movie = relationship('Movies',backref=backref('hallschedules', lazy=True))
#
# # 座位
# class Seats(db.Model):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     seattype = Column(Enum(0, 1, 2))  # 座位类型(0普通、1沙发、2豪华)
#     x = Column(Integer)  # x坐标
#     y = Column(Integer)  # y坐标
#     is_sale = Column(Boolean,default=True)  # 当前排期是否可卖
#     flag = Column(Integer)  # 状态(损坏0、正常1)
#     is_delete = Column(Boolean,default=False)  # 是否删除
#
#     # 与影院的关系
#     cinemaid = Column(Integer, ForeignKey('cinemas.id'))
#     cinema = relationship('Cinemas', backref=backref('seats', lazy=True))
#     # 与影厅的关系
#     hallid = Column(Integer, ForeignKey('halls.id'))
#     hall = relationship('Halls', backref=backref('seats', lazy=True))