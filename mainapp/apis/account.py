import random
import uuid
from datetime import datetime
from flask import request
from flask_mail import Message
from flask_restful import Resource, reqparse, fields, marshal
import mainapp.ext
from mainapp import dao, helper
from mainapp.models import User, db


class AccountApi(Resource):
    parser = reqparse.RequestParser()
    # opt操作：active激活账号，login登录，changepwd改密，
    # findpwd找回密码，logout退出，reactive重新激活
    parser.add_argument('opt',dest='opt',required=True,help='请声明opt操作')

    # 账号激活，重新申请激活，退出
    def get(self):
        #从请求参数中获取opt和token值
        #如果opt为active，则从redis中取出token的值即用户id
        # 如果用户id存在 ，则将用户的is_active改为True
        args = self.parser.parse_args()
        opt = args.get('opt')

        # 账号激活
        if opt == 'active':
            active = self.parser.copy()
            active.add_argument('token', required=True, dest='token', help='请提供激活账号的token')
            args = active.parse_args()
            token = args.get('token')
            id = mainapp.ext.cache.get(token)
            if id:
                user = dao.getById(User,id)
                user.is_active = True  #修改账号激活状态
                if dao.save(user) : #提交修改
                    mainapp.ext.cache.delete(token)  #激活成功删除token
                    return {'msg':'用户 {} 的账号已激活成功!'.format(user.name)}
            else:
                reactive_url = request.host_url + 'account/?opt=reactive'
                return {'msg':'激活时间已过期,请前往此地址：{} 重新激活!'.format(reactive_url)}

        # 用户退出
        elif opt == 'logout':
            # 退出登录
            mainapp.ext.cache.delete_many('token', 'userid')
            return {'status': 700, 'msg': '退出成功!'}  #700,操作成功

        # 重新激活
        elif opt == 'reactive':
            return self.reactive()

    # 修改密码
    def put(self):
        args = self.parser.parse_args()
        opt = args.get('opt')
        if opt == 'changepwd':  # 修改密码
            return self.changepwd()

    # 用户登录，找回密码
    def post(self):
        args = self.parser.parse_args()
        opt = args.get('opt')
        if opt == 'login':  # 登录
            return self.login()
        elif opt == 'findpwd':  # 找回密码
            return self.findpwd()

    # 封装重新申请账号激活函数
    def reactive(self):
        active = self.parser.copy()
        active.add_argument('email', required=True, dest='email', help='请提供email账号')
        args = active.parse_args()
        email = args.get('email')
        qs = dao.query(User).filter(User.email.__eq__(email))
        if qs.count():
            helper.sendMail(qs.first())  #发送邮件激活账号
            return {'status':700,'msg':'重新申请激活账号成功，请前往邮箱激活账号!'}
        else:
            # 700，信息验证错误
            return {'status':701,'msg':'申请失败，请确认email账号是否输入正确!'}

    # 封装用户登录函数
    def login(self):
        # 需提供用户名，密码
        # 从数据库查找到用户，生成token，将用户名存储，设置一定的时间，可以不用再登录
        login = self.parser.copy()
        login.add_argument('name', dest='username', required=True, help='请提供用户名')
        login.add_argument('passwd', dest='passwd', required=True, help='请提供密码')
        args = login.parse_args()
        name = args.get('username')
        passwd = helper.md5_crypt(args.get('passwd'))
        qs = dao.query(User).filter(db.and_(User.name == name, User.passwd == passwd)).first()
        print(qs)
        if qs:
            # 判断用户是否激活，如果激活了就可以登录，否则要先激活
            if qs.is_active:
                # 修改用户登录时间
                qs.last_login_time = datetime.now()
                dao.save(qs)
                # 生成token
                token = helper.getToken()
                # 将token和用户id存入缓存中,因为id可以直接get取信息,token可以判断登录状态
                mainapp.ext.cache.set('token', token, timeout=60 * 60 * 24 * 3)  # 有效时间是3天
                mainapp.ext.cache.set('userid', qs.id, timeout=60 * 60 * 24 * 3)

                out_user_fields = {
                    'name':fields.String,
                    'phone':fields.String,
                    'email':fields.String,
                    'photo':fields.String(attribute='photo_1')
                }

                out_fields = {
                    'status':fields.String(default=700),
                    'datas':fields.Nested(out_user_fields),
                    'token': fields.String
                }

                data = {'datas':qs,
                        'msg': '用户 {} 登录成功!'.format(qs.name),
                        'token':token}

                return marshal(data,out_fields)
            else:
                reactive_url = request.host_url + 'account/?opt=reactive'
                return {'status': 701,'msg': '帐号未激活,请前往此地址：{} 激活账号!'.format(reactive_url)}
        else:
            return {'status': 702, 'msg': '对不起，登录失败，请确认用户名或密码是否正确'}

    # 封装用邮箱找回密码函数
    def findpwd(self):
        find = self.parser.copy()
        # 忘记密码，需要输入邮箱，会给邮箱发送一个临时密码，然后让用户登陆上去再把密码修改
        find.add_argument('email', dest='email', required=True, help='请提供邮箱')
        args = find.parse_args()

        # 用邮箱找回密码
        # 找回密码，先根据邮箱(邮箱唯一)查到用户，对其修改一个随机六位密码
        # 用邮件发给用户，让用户先登录，再修改密码
        user = dao.query(User).filter(User.email == args.get('email')).first()
        if user:
            l = list('asdq34rg025nqrb0929345pjq3')
            i = 0
            s = ''
            # 随机生成6位暂时的密码
            while i < 6:
                index = random.randint(0, len(l)-1)
                s += l[index]
                i += 1
            # print(s)
            user.passwd = helper.md5_crypt(s)
            dao.save(user)  # 随机生成的密码保存
            # 发送邮件
            msg = Message(subject='用户密码找回-淘票票后台管理系统',  # 邮箱主题
                          recipients=[user.email],  # 收件人，必须是列表类型
                          sender='disenqf@163.com')  # 发件方
            msg.html = "<h3>{} 您好,您正在进行密码找回操作,这是为您暂时生成的6位随机密码：<em>{}</em>,请登录后及时修改密码!</h3>".format(user.name, s)
            mainapp.ext.mail.send(msg)
            return {'status': 700, 'msg': '密码找回成功，请前往邮箱查看新密码!'}
        return {'status': 701, 'msg': '密码找回失败，请确认邮箱是否输入正确!'}

    # 封装修改密码函数
    def changepwd(self):
        # 修改密码与密码找回
        # put请求是密码时，则为修改密码(登录状态)，请求时邮箱时，则为找回密码(未登录)
        change = self.parser.copy()
        change.add_argument('oldpwd', required=True, dest='oldpwd', help='请提供原密码')
        change.add_argument('newpwd', required=True, dest='newpwd', help='请提供新密码')
        args = change.parse_args()

        oldpwd = helper.md5_crypt(args.get('oldpwd'))  # 拿到新密码
        newpwd = helper.md5_crypt(args.get('newpwd'))  # 拿到新密码
        # 修改密码操作
        userid = mainapp.ext.cache.get('userid')  # 从缓存中取用户id
        if userid:
            user = dao.getById(User, userid)
            if user.passwd == oldpwd:  # 判断原密码是否输入正确
                user.passwd = newpwd  # 修改密码
                dao.save(user)
                return {'status': 700, 'msg': '密码修改成功!'}
            else:
                return {'status': 701, 'msg': '密码修改失败，请确认原密码是否输入正确!'}
        else:
            return {'status': 702, 'msg': '请先登录!'}  #702，查询不到信息
