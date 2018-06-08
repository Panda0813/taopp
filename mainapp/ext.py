# 集成第三方内容
from flask_cache import Cache
from flask_mail import Mail
from mainapp.apis import init_api
from mainapp.models import init_db

mail = Mail()

# 配置cache缓存,可以配置多个cache用来存储不同的信息
cache = Cache(config={
    'CACHE_TYPE':'redis',
    'CACHE_REDIS_HOST':'10.35.163.30',
    'CACHE_REDIS_PORT':'6379',
    'CACHE_REDIS_DB':12,
})

def init_ext(app):
    init_db(app)  #初始化数据库

    init_api(app)  #初始化api接口

    mail.init_app(app)  #初始化邮箱模块

    cache.init_app(app)  #初始化缓存