import os
from flask_restful import Api
from mainapp.apis.account import AccountApi
from mainapp.apis.cinemas import CinemasApi
from mainapp.apis.city import CityApi
from mainapp.apis.movies import MoviesApi
from mainapp.apis.upload import UploadApi
from mainapp.apis.user import UserApi

api = Api()  #创建 RESTful的Api对象

# 初始化app
def init_api(app):
    api.init_app(app)

api.add_resource(CityApi,'/city/')
api.add_resource(UserApi,'/user/')
api.add_resource(AccountApi,'/account/')
# api.add_resource(UserLoginApi,'/login/')
api.add_resource(MoviesApi,'/movies/')
api.add_resource(UploadApi,'/upload/')
api.add_resource(CinemasApi,'/cinemas/')


