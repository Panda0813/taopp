from flask_restful import Resource, fields, marshal_with, reqparse
from flask_sqlalchemy import BaseQuery

from mainapp import dao
from mainapp.models import Cinemas


class CinemasApi(Resource):
    cinemas_fields = {
        'name': fields.String,
        'city': fields.String,
        'district': fields.String,
        'address': fields.String,
        'phone': fields.String,
        'score': fields.Float,
        'hallnum': fields.Integer,
        'servicecharge': fields.Float,
        'astrict': fields.Integer,
        'flag': fields.Integer,
        'isdelete': fields.Boolean
    }

    out_fields = {
        "returnCode": fields.String(default='0'),
        "msg":fields.String(default=''),
        "returnValue": fields.Nested(cinemas_fields)
    }



    @marshal_with(out_fields)
    def get(self):
        # 定制输入
        parser = reqparse.RequestParser()
        parser.add_argument('city',required=True,help='请提供城市city参数')
        parser.add_argument('area',dest='district',help='请提供区域参数')
        parser.add_argument('sort',type=int,default=1)  #排序默认降序
        parser.add_argument('orderby',default='score')  #排序方式,默认以影院评分排序
        parser.add_argument('page',type=int,default=1,help='页码必须为int类型')  #默认第一页
        parser.add_argument('count',type=int,default=5,help='页码必须为int类型')  #默认每页5个影院

        args = parser.parse_args()
        # 当前城市的所有影院
        qs:BaseQuery = dao.query(Cinemas).filter(Cinemas.city == args.get('city'))
        # 当前区域的所有影院
        # 如果没指定区域，就显示该城市的所有影院
        district = args.get('district')
        if district:
            qs:BaseQuery = qs.filter(Cinemas.district == district)

        #对影院进行排序
        sort = args.get('sort')
        qs: BaseQuery = qs.order_by(('-' if sort == 1 else '')+args.get('orderby'))

        #分页
        pager = qs.paginate(args.get('page'),args.get('count'))

        return {"returnValue": pager.items}