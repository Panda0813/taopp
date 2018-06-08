# import random
# import uuid
# from datetime import datetime
#
# from flask import request
# from flask_mail import Message
# from flask_restful import Resource, reqparse
# from mainapp import dao, helper
# from mainapp.models import User, db
# import mainapp.ext
#
# class UserLoginApi(Resource):
#     #定制输入
#     parser = reqparse.RequestParser()
#     # opt操作：login登录，changepwd改密，findpwd找回密码，logout退出
#     parser.add_argument('opt',required=True,help='请声明opt操作')
#
#     # 用户登录
#     def post(self):
#         args = self.parser.parse_args()
#         opt = args.get('opt')
#         if opt == 'login':  #登录
#             return self.login()
#         elif opt == 'findpwd':  #找回密码
#             return self.findpwd()
#
#     # 封装用户登录函数
#     def login(self):
#         # 需提供用户名，密码
#         # 从数据库查找到用户，生成token，将用户名存储，设置一定的时间，可以不用再登录
#         login = self.parser.copy()
#         login.add_argument('name', dest='username', required=True, help='请提供用户名')
#         login.add_argument('passwd', dest='passwd', required=True, help='请提供密码')
#         args = login.parse_args()
#         name = args.get('username')
#         passwd = helper.md5_crypt(args.get('passwd'))
#         qs = dao.query(User).filter(db.and_(User.name == name, User.passwd == passwd)).first()
#         print(qs)
#         if qs:
#             if qs.is_active:
#                 # 修改用户登录时间
#                 qs.last_login_time = datetime.now()
#                 dao.save(qs)
#                 # 生成token
#                 token = helper.md5_crypt(str(uuid.uuid4()))
#                 # 将token和用户id存入缓存中,因为id可以直接get取信息,token可以判断登录状态
#                 mainapp.ext.cache.set('token', token, timeout=60 * 60 * 24 * 3)  # 有效时间是3天
#                 mainapp.ext.cache.set('userid', qs.id, timeout=60 * 60 * 24 * 3)
#                 return {'status': 200, 'msg': '用户 {} 登录成功!'.format(qs.name)}
#             else:
#                 reactive_url = request.host_url + 'account/?opt=reactive'
#                 return {'msg': '帐号未激活,请前往此地址：{} 激活账号!'.format(reactive_url)}
#         else:
#             return {'status': 201, 'msg': '对不起，登录失败，请确认用户名或密码是否正确'}
#
#     # 封装用邮箱找回密码函数
#     def findpwd(self):
#         find = self.parser.copy()
#         # 忘记密码，需要输入邮箱，会给邮箱发送一个临时密码，然后让用户登陆上去再把密码修改
#         find.add_argument('email', dest='email', required=True, help='请提供邮箱')
#         args = find.parse_args()
#
#         # 用邮箱找回密码
#         # 找回密码，先根据邮箱(邮箱唯一)查到用户，对其修改一个随机六位密码
#         # 用邮件发给用户，让用户先登录，再修改密码
#         user = dao.query(User).filter(User.email == args.get('email')).first()
#         if user:
#             l = list('asdq34rg025nqrb0929345pjq3')
#             i = 0
#             s = ''
#             # 随机生成6位暂时的密码
#             while i < 6:
#                 index = random.randint(0, len(l))
#                 s += l[index]
#                 i += 1
#             # print(s)
#             user.passwd = helper.md5_crypt(s)
#             dao.save(user)  # 随机生成的密码保存
#             # 发送邮件
#             message= ('用户密码找回-淘票票后台管理系统',  # 邮箱主题
#                           [user.email],  # 收件人，必须是列表类型
#                           'disenqf@163.com')  #发件方
#             html = "<h3>{} 您好,您正在进行密码找回操作,这是为您暂时生成的6位随机密码：<em>{}</em>,请登录后及时修改密码!</h3>".format(user.name, s)
#             self.sendmsg(message,html)
#             return {'status': 200, 'msg': '密码找回成功，请前往邮箱查看新密码!'}
#         return {'status':201,'msg':'密码找回失败，请确认邮箱是否输入正确!'}
#
#     def put(self):
#         args = self.parser.parse_args()
#         opt = args.get('opt')
#         if opt == 'changepwd':  # 修改密码
#             return self.changepwd()
#
#     # 封装修改密码函数
#     def changepwd(self):
#         # 修改密码与密码找回
#         # put请求是密码时，则为修改密码(登录状态)，请求时邮箱时，则为找回密码(未登录)
#         change = self.parser.copy()
#         change.add_argument('passwd', required=True, dest='oldpwd', help='请提供原密码')
#         change.add_argument('passwd',required=True, dest='newpwd', help='请提供新密码')
#         args = change.parse_args()
#
#         oldpwd = helper.md5_crypt(args.get('oldpwd'))  # 拿到新密码
#         newpwd = helper.md5_crypt(args.get('newpwd'))  # 拿到新密码
#         # 修改密码操作
#         userid = mainapp.ext.cache.get('userid')  # 从缓存中取用户id
#         if userid:
#             user = dao.getById(User, userid)
#             if user.passwd == oldpwd:  #判断原密码是否输入正确
#                 user.passwd = newpwd  # 修改密码
#                 dao.save(user)
#                 return {'status': 200, 'msg': '密码修改成功!'}
#             else:
#                 return {'status':201,'msg':'密码修改失败，请确认原密码是否输入正确!'}
#         else:
#             return {'status': 201, 'msg': '请先登录!'}





