#encoding=utf8
__author__ = 'paul'

# input: image and xls data folder
# function: dump data to DB and form item for shops in each city
# warning: image name must map item name in xls data

import json
from pymongo import MongoClient
import time
import os
import os.path
import xlrd
from dumpPNGImageToMongoDB import mongoImg
# =============input======================
db_name = 'test01'
image_path = './image/'
file_path = './data/'
con = MongoClient(host='mongodb://paul:test@localhost/admin')
# ===================================


db = con[db_name]
col_category = db.category
col_shop = db.shop
db_fs = con['db-fs']
col_image = db_fs['fs.files']
col_item = db.item


#['school', 'camp', 'num', 'pro', 'city', 'lng', 'lat', 'name', 'mobile', 'description']
# json - dic_city_sch(camp,school)
def formCitySchoolDic():
    data = json.loads(file('./schoolsData.json').read())
    dic_city_sch = {}
    for each in data:
        schs = dic_city_sch.setdefault(each.get('city'), [])
        info = (each.get('school'), each.get('camp'))
        if info not in schs:
            schs.append(info)
    return dic_city_sch

# parse data path - list_city
def ParseDataFromExcel(_file,city):
    book = xlrd.open_workbook(file_contents=file(_file).read())
    sh0 = book.sheet_by_index(0)
    dic_city_item = {}
    items = dic_city_item.setdefault(city, [])
    for i in range(1,sh0.nrows):
        row=sh0.row(i)
        item = []
        for j in range(2):
            item.append(row[j].value)
        item.append(i)
        if item not in items:
            items.append(item)
    return dic_city_item
def ParseDataPath(filepath):
    files = []
    files_p = []
    list_city = []
    temp_dic = []
    temp = []
    for r,d,f in os.walk(filepath):
        files = f
    for ff in f:
        files_p.append(os.path.join(filepath, ff))
    for filename in files:
        list_city.append(filename.split('.')[0].decode('utf8'))
    # parse data - dic_city_item(name,price)
    for f in files_p:
        city = os.path.basename(f).split('.')[0].decode('utf8')
        try:
            temp_dic.append(ParseDataFromExcel(f, city))
        except Exception,e:
            print e
    for each in temp_dic:
        temp += each.items()
    return dict(temp), list_city


# dic_city_sch & list_city & school DB - sch+camp+烟店 & category & dic_city_shopId
def formShopAndItsCate(dic_city_sch, list_city):
    image_id = ''
    dic_city_shopId = {}
    for city in list_city:
        schs = dic_city_sch.get(city)
        if not schs:
            print 'no school in ',city#.encode('utf8')
            continue
        list_schs_id = dic_city_shopId.setdefault(city, [])
        for _sch in schs:
            name = _sch[0]
            camp = _sch[1]
            cond = {
                'school': name,
                'camp': camp
            }
            sch = db.school.find_one(cond)
            cond = {}
            shop_name = sch.get('school') + sch.get('camp')
            cond['school_district'] = sch.get('_id')
            cond['image_id'] = image_id
            cond['name'] = sch.get('school') + sch.get('camp') + u'烟店'
            if sch.get('location') :
                cond['location'] = [float(sch.get('location')[0]), float(sch.get('location')[1])]
            cond['mobile'] = sch.get('mobile')
            cond['address'] = sch.get('address')
            cond['status'] = 'open'
            cond['created_time'] = int(time.time()*1000)
            cond['open_hour'] = [0, 86400]
            cond['delivery_price'] = 100
            cond['min_cost_to_deliver'] = 0
            cond['type'] = 'cvs'
            sid = col_shop.insert(cond)
            list_schs_id.append(sid)
            # form shop category
            cats = ['烟']
            for j in range(len(cats)):
                cond = {}
                cond['name'] = cats[j]
                cond['priority'] = 1 # last to show
                cond['shop_id'] = sid
                col_category.insert(cond)
    return dic_city_shopId
#dic_city_shopId & dic_city_item - item
def dumpItemImage(db_fs, _path):
    di = mongoImg(db_fs, _path)
    di.insert()
def formShopItem(dic_city_shopId, dic_city_items,list_city):
    for city in list_city:
        sids = dic_city_shopId.get(city)
        if sids:
            for sid in sids:
                items = dic_city_items.get(city)
                if items:
                    for item in items:
                        cond = {}
                        cond['name'] = item[0]
                        cond['price'] = int(item[1]*100)
                        cond['shop_id'] = sid
                        cond['created_time'] = int(time.time()*1000)
                        cond['status'] = 'on_sale'
                        cond['description'] = ''
                        cond['priority'] = item[2]
                        image_id = col_image.find_one({'filename': item[0]}).get('_id')
                        if image_id:
                            cond['image_id'] = image_id
                        else:
                            print 'no image for ', item[0]#.encode('utf8')
                        cate = col_category.find_one({'shop_id': sid})['_id']
                        if cate:
                            cond['category'] = cate
                        else:
                            print 'no category in shop_id', str(sid)
                        col_item.insert(cond)
                else:
                    print 'no item in ', city#.encode('utf8')
        else:
            print 'no shop in', city#.encode('utf8')


dic_city_schCamp = formCitySchoolDic()
print len(dic_city_schCamp)
(dic_city_items, list_city) = ParseDataPath(file_path)
print list_city
dic_city_shopId = formShopAndItsCate(dic_city_schCamp, list_city)
dumpItemImage(db_fs, image_path)
formShopItem(dic_city_shopId, dic_city_items, list_city)