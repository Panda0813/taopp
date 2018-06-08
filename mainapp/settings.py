import os
class Config():
    ENV = 'development'
    DEBUG = True

    SECRET_KEY = 'a4q2435rg#$@1dfq45y35'

    #配置数据库连接
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@10.35.163.30:3306/taopp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #配置邮箱
    MAIL_SERVER = 'smtp.163.com'  #邮箱服务器
    MAIL_USERNAME = '18700469641@163.com'
    MAIL_PASSWORD = 'zyw0813'  #授权码


# 配置静态资源路径
BASE_DIR = os.path.dirname(os.path.abspath(__name__))
STATIC_DIR = os.path.join(BASE_DIR, 'mainapp\static')
MEDIA_ROOT = os.path.join(STATIC_DIR, 'uploads')


# 用户权限的配置
class QX():
    QUERY_QX = 1
    EDIT_QX = 2
    DELETE_QX = 4
    ADD_QX = 8
    MAIL_QX = 16
    PLAY_QX = 32