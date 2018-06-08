import json
import pymysql
with open('cities.json','rb') as f:
    cities = json.load(f)  #加载json数据
    print(type(cities))
    print(cities)

    db = pymysql.connect(host='10.35.163.30',
                         port=3306,
                         user = 'root',
                         password='root',
                         db='taopp',
                         charset='utf8')
    print('数据库连接成功!')
    cursor = db.cursor()

    # 所有内容
    values = cities.get('returnValue')
    for letter in values.keys():
        cursor.execute('insert t_letter(name) values(%s)', letter)
        db.commit()
        cursor.execute('select id from t_letter where name = %s', letter)
        letter_id = cursor.fetchone()[0]
        print('添加成功',cursor.fetchone())
        for city in values.get(letter):
            cursor.execute('insert t_city values(%s,%s,%s,%s,%s,%s)',
                           (city.get('id'),
                            city.get('parentId'),
                            city.get('regionName'),
                            city.get('cityCode'),
                            city.get('pinYin'),
                            letter_id))

        db.commit()
