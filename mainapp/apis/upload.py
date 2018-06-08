import uuid
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
import mainapp.ext
from mainapp import helper, dao
from mainapp.models import User


class UploadApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file',dest='file',
                        type=FileStorage,
                        required=True,
                        location = 'files',
                        help='请提供要上传的资源')

    def post(self):
        args = self.parser.parse_args()
        upFile:FileStorage = args.get('file')

        # 先判断用户是否登录，如果登录了才能上传头像
        if self.judgeLogin():
            # 获取并拼接文件扩展名
            extName = '.'+ upFile.filename.split('.')[-1]
            # 生成新的文件名
            newFileName = str(uuid.uuid4())+extName
            # 拼接资源保存路径
            fileSavePath = helper.uploadPath(newFileName)
            print('保存路径--->', helper.uploadPath(newFileName))
            upFile.save(fileSavePath)
            upFile.close()

            path = '/static/uploads/'+newFileName
            u = self.judgeLogin()
            u.photo_1 = path
            dao.save(u)
            return {'status':700,'msg': '{} 头像上传成功,已保存至：{}'.format(u.name,path)}

        # 未登录，返回信息
        return {'status':702,'msg':'请先登录!'}

    #判断用户是否登录
    def judgeLogin(self):
        userid = mainapp.ext.cache.get('userid')  #从缓存中取出用户id
        if userid:
            return dao.getById(User,userid)
        else:
            return False