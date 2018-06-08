from flask import request
from flask_restful import Resource, fields, reqparse, marshal_with
from flask_sqlalchemy import BaseQuery
from mainapp import dao
from mainapp.models import Movies, User, Qx
import mainapp.ext
from mainapp.settings import QX

def check_login(qx):
    def check(fun):
        def wrapper(*args,**kwargs):
            print('--check login--')

            # 从缓存中获取登录用户的token
            userid = mainapp.ext.cache.get('userid')
            if not userid:
                return {'status': 701, 'msg': '请先登录'}
            loginUser: User = dao.getById(User, userid)

            # 删除影片功能
            # 先判断登录用户是否有删除权限
            if loginUser.rights & qx == qx:
                return fun(*args, **kwargs)
            else:
                qval = dao.query(Qx).filter(Qx.right == qx).first()
                return {'status': 701, 'msg': '对不起，您没有 {} 权限!'.format(qval.name)}
        return wrapper
    return check

class MoviesApi(Resource):
    # 定制输出
    movie_fields ={
        'id': fields.Integer,
        'showname': fields.String,
        'shownameen': fields.String,
        'director': fields.String,
        'leadingRole': fields.String,
        'type': fields.String,
        'country': fields.String,
        'language': fields.String,
        'duration': fields.Integer,
        'screeningmodel': fields.String,
        'openday': fields.DateTime,
        'backgroundpicture': fields.String,
        'flag': fields.Integer,
        'isdelete': fields.Boolean
    }


    out_fields = {
        "returnCode": fields.String(default='0'),
        "returnValue": fields.Nested(movie_fields)
    }


    @marshal_with(out_fields)
    def get(self):
        # 定制输入方法
        parser = reqparse.RequestParser()

        parser.add_argument('flag',dest='flag',type=int,required=True,help='请提供flag参数')
        parser.add_argument('sort', dest='sort', type=int, default=1)  # 默认降序
        parser.add_argument('orderby', default='openday')  # 默认以上映时间排序
        parser.add_argument('page', dest='page', type=int, default=1, help='页码必须为int类型')
        parser.add_argument('limit', dest='limit', type=int, default=20, help='每页显示数量')

        # 查看影片
        args = parser.parse_args()
        # 根据影片状态查到影片
        qs: BaseQuery = dao.query(Movies).filter(Movies.flag == args.get('flag'))

        # 排序
        sort = args.get('sort')
        qs: BaseQuery = qs.order_by(('-' if sort == 1 else '')+args.get('orderby'))

        # 分页
        pager = qs.paginate(args.get('page'),args.get('limit'))
        return {"returnValue": pager.items}

    @check_login(QX.DELETE_QX)
    def delete(self):
        mid = request.args.get('mid')
        # 从缓存中获取登录用户的token
        # userid = mainapp.ext.cache.get('userid')
        # if not userid:
        #     return {'status':701,'msg':'请先登录'}
        #
        # loginUser:User = dao.getById(User,userid)
        #
        # # 删除影片功能
        # # 先判断登录用户是否有删除权限
        # if loginUser.rights & QX.DELETE_QX == QX.DELETE_QX:
        movie = dao.getById(Movies,mid)
        if not movie:
            return {'status': 701, 'msg': '要删除的影片资源不存在'}

        # 删除
        dao.delete(movie)
        return {'status':700,'msg':'删除成功!'}
