#encoding=utf8
from pymongo import MongoClient
import time,datetime

startTime=datetime.datetime(2014,8,15,0,0,0)
endTime=datetime.datetime(2014,11,30,23,59,59)
startTime=time.mktime(startTime.timetuple())*1000
endTime=time.mktime(endTime.timetuple())*1000

url='mongodb://192.168.1.110/'
con=MongoClient(url)
db=con['20141205']
url_bank='localhost'
con_bank=MongoClient(url_bank)
db_bank=con_bank['self']
results=[]
for each in db.withdraw.find({'created_time':{'$gte':startTime,'$lte':endTime}}):
    shop_id=str(each['shop_id'])
    shop_mobile=db.shop.find_one({'_id':each['shop_id']},{'mobile':1})['mobile']
    shop_name=db.shop.find_one({'_id':each['shop_id']},{'name':1})['name'].encode('utf8')
    shop_owner=db.shop.find_one({'_id':each['shop_id']},{'withdraw.name':1})['withdraw']['name'].encode('utf8')
    line=shop_id+'\t'+shop_name+'\t'+str(shop_mobile)+'\t'+shop_owner+'\t'+str(each['_id'])+'\t'+time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(each['created_time']/1000))+'\t'+str(each['account'])+'\t'+each['name'].encode('utf8')+'\t'+str(each['money'])+'\t'+'\xe5\x95\x86\xe6\x88\xb7\xe6\x8f\x90\xe7\x8e\xb0'
    bank=db_bank['test01'].find_one({'id':each['account']},{'_id':0})
    if bank!=None:
        #print bank['type'].encode('utf8')
        #print bank['lt'].encode('utf8')
        if len(bank['lt'].split('-'))==2:
            line+='\t'+bank['type'].encode('utf8').split('-')[0]+'\t\t'+bank['lt'].encode('utf8').split('-')[0]+'\t'+bank['lt'].encode('utf8').split('-')[1]+'\n'#\t银行\t\t省\t市\n
        else:
            line+='\t'+bank['type'].encode('utf8').split('-')[0]+'\t\t'+bank['lt'].encode('utf8')+'\t'+bank['lt'].encode('utf8')+'\n'
    else: 
        line+='\t-\t\t-\t-\n'
    results.append(line)
f=open('./bank_list.xls','wb')
f.writelines(results)
f.close()
    
    