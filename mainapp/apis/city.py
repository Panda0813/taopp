from flask_restful import Resource, fields, marshal_with
from mainapp import dao
from mainapp.models import Letter


class CityApi(Resource):
    #城市字段，从value_fields调用到这里，将cities解析
    city_fields = {
        'id':fields.Integer,
        'parentId':fields.Integer,
        'regionName':fields.String,
        'cityCode':fields.Integer,
        'pinYin':fields.String
    }
    #字母和城市，传入cities，再调用city_fields解析
    value_fields = {
        # '字母':fields.Nested(city_fields)
    }
    #最终输出字段，调用value_fields解析
    out_fields = {
        'returnCode':fields.String(default='0'),
        'returnValue':fields.Nested(value_fields)
    }

    @marshal_with(out_fields)
    def get(self):
        letters = dao.queryAll(Letter)
        returnValue = {}
        for letter in letters:
            # 动态修改属性
            self.value_fields[letter.name] = fields.Nested(self.city_fields)
            returnValue[letter.name] = letter.cities  # 就是最后的city_fields

        return {'returnValue':returnValue}


