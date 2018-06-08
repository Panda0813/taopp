# 定义操作数据库的功能函数
from flask_sqlalchemy import BaseQuery
from mainapp.models import db


def query(cls) -> BaseQuery:
    # 返回基于某一个类的查询
    return db.session.query(cls)

def queryAll(cls):
    return query(cls).all()

def getById(cls,id):
    #获取指定id的数据
    try:
        return query(cls).get(id)
    except:
        pass

# def queryByKey(cls,**key):
#     return query(cls).filter_by()

def save(obj) -> bool:
    try:
        db.session.add(obj)
        db.session.commit()
    except:
        return False
    return True

def delete(obj) -> bool:
    try:
        db.session.delete(obj)
        db.session.commit()
    except:
        return False
    return True