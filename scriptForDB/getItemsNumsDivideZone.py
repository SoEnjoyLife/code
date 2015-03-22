#encoding=utf8
__author__ = 'paul'
from login import db
from datetime import datetime
from datetime import timedelta
import time
import xlwt

#each file divide by month
#divide by zone
#line in each sheet: name, sale_num
status = ['paid','preparing_items','delivering_items','confirmed','success']
startTime = time.mktime(datetime(2014,12,1,0).timetuple())*1000
endTime = time.mktime(datetime(2015,1,1,0).timetuple())*1000

condition = {
    'created_time': {
        '$gte': startTime,
        '$lte': endTime
    },
    'status': {'$in': status},

}
#each = db.order.find_one()
zone_item__num = {}
for each in db.order.find(condition):
    #print each
    items = each.get('items','')
    #print items
    for item in items:
        item_id = item.get('_id','')
        _item = db.item.find_one({'_id':item_id})
        #item_name = _item.get('name').encode('utf8')
        item_name = _item.get('name')
        item_zone_id = _item.get('zone_id')
        item_num = {}
        if item_zone_id:
            name = db.zone.find_one({'_id':item_zone_id}).get('name')
            if name:
                item_num = zone_item__num.setdefault(name, {})
                num = item_num.setdefault(item_name, 0)
                item_num[item_name] = num + 1
            else:
                item_num = zone_item__num.setdefault(u'unknow', {})
                num = item_num.setdefault(item_name, 0)
                item_num[item_name] = num + 1
        else:
            item_num = zone_item__num.setdefault(u'unknow', {})
            num = item_num.setdefault(item_name, 0)
            item_num[item_name] = num + 1

#print zone_item__num
print len(zone_item__num)
w = xlwt.Workbook()
for zone, item_num in zone_item__num.items():
    ws = w.add_sheet(zone)
    ws.write(0, 0, 'item')
    ws.write(0, 1, 'sales_num')
    row = 1
    sorted_item = sorted(item_num.iteritems(), key=lambda x: x[1])
    # for i, n in item_num.items():
    #     ws.write(row, 0, i)
    #     ws.write(row, 1, n)
    for each in sorted_item:
        ws.write(row,0,each[0])
        ws.write(row,1,each[1])
        row +=1
w.save(u'单量2014-12.xls')




