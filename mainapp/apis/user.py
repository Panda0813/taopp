from flask import request
from flask_restful import Resource, reqparse

import tasks
from mainapp import helper, dao
from mainapp.models import User


class UserApi(Resource):
    #定制输入字段
    parser = reqparse.RequestParser()
    parser.add_argument('name',dest='name',required=True,help='用户名不能为空')

    def post(self):
        #从基本的公共请求解析器中复制一份
        register = self.parser.copy()
        #在添加到注册时使用
        register.add_argument('passwd', dest='pwd', required=True, help='密码不能为空')
        register.add_argument('email',dest='email', required=True, help='邮箱不能为空')
        register.add_argument('nickname', dest='nickname', required=True, help='昵称不能为空')
        register.add_argument('phone', dest='phone',required=True, help='电话不能为空')

        #将输入字段存放入args
        args = register.parse_args()

        u = User()
        u.name = args.get('name')
        u.nickname = args.get('nickname')
        u.phone = args.get('phone')
        u.email = args.get('email')
        u.passwd = helper.md5_crypt(args.get('pwd'))

        if dao.save(u):
            #发送邮件激活账号
            # helper.sendMail(u)
            tasks.sendMail.delay(request.host_url,u.id)
            return {'status':200,'msg':'用户注册成功!'}
        else:
            return {'status': 201, 'msg': '用户注册失败!'}

    def get(self):
        # 验证用户名是否已注册
        args = self.parser.parse_args()
        name = args.get('name')
        #在数据库中查询这个用户名
        q = dao.query(User).filter(User.name == name)
        if q.count():
            return {'status': 202, 'msg': '用户名{}已存在'.format(name)}
        else:
            return {'status': 200, 'msg': '用户名可注册!'}

