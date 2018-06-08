from celery import Celery
from flask import request
from flask_mail import Message

from mainapp import dao
from mainapp.helper import getToken
import mainapp.ext
from mainapp.models import User

try:
    import manage
except:
    pass

celery = Celery('tasks',
                # include=['manage'],
                broker='redis://10.35.163.30:6379/5')

@celery.task
def sendMail(url,uId):
    # try:
    #     import manage
    # except:
    #     pass
    # global manage
    with manage.app.test_request_context():
        u = dao.getById(User,uId)
        # 生成token
        token = getToken()
        # 将token存入redis中
        mainapp.ext.cache.set(token, u.id, timeout=600)  # 允许10分钟内去邮箱激活账号

        # 设置激活链接
        active_url = url + 'account/?opt=active&token=' + token
        msg = Message(subject='淘票票用户账号激活',  # 邮箱主题
                      recipients=[u.email],  # 收件人，必须是列表类型
                      sender='18700469641@163.com')
        msg.html = "<h1>恭喜用户 {} 注册成功,欢迎加入!</h1>" \
                   "<h3>点击 <a href={}> 激活 </a> 您的账号</h3><h3>或复制此地址 {} 到浏览器进行激活</h3>".format(u.name, active_url,
                                                                                            active_url)
        try:
            mainapp.ext.mail.send(msg)
            print('邮件发送成功!')
        except Exception as e:
            print(e)
            print('邮件发送失败!')
