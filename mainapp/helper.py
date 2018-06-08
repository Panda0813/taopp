#自定义工具类
import hashlib
import uuid

import os
from flask import request
import mainapp.ext
#MD5加密
from flask_mail import Message

from mainapp import settings


def md5_crypt(txt):
    m = hashlib.md5()
    m.update(txt.encode())
    return m.hexdigest()

def getToken():
    return md5_crypt(str(uuid.uuid4()))

# 发送邮件激活用户账号
# def sendMail(qs):  # qs是用户对象
#     # 生成token
#     token = getToken()
#     # 将token存入redis中
#     mainapp.ext.cache.set(token, qs.id, timeout=600)  # 允许10分钟内去邮箱激活账号
#
#     # 设置激活链接
#     active_url = request.host_url + 'account/?opt=active&token=' + token
#     msg = Message(subject='淘票票用户账号激活',  #邮箱主题
#                   recipients=[qs.email],  #收件人，必须是列表类型
#                   sender='18700469641@163.com')
#     msg.html = "<h1>恭喜用户 {} 注册成功,欢迎加入!</h1>" \
#                "<h3>点击 <a href={}> 激活 </a> 您的账号</h3><h3>或复制此地址 {} 到浏览器进行激活</h3>".format(qs.name,active_url,active_url)
#     mainapp.ext.mail.send(msg)

def uploadPath(filename):
    return os.path.join(settings.MEDIA_ROOT,filename)
