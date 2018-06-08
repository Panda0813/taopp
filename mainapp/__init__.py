from flask import Flask
from mainapp import settings
from mainapp.ext import init_ext


def create_app():
    app = Flask(__name__)
    # 配置
    app.config.from_object(settings.Config)

    #初始化第三方命令
    init_ext(app)

    return app