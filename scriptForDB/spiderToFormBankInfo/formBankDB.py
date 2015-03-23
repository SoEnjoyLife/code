#encoding=utf-8
from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib2
from pymongo import MongoClient
import traceback
from random import choice
import datetime,time
import thread
from os.path import exists



startTime=datetime.datetime(2014,8,15,0,0,0)
endTime=datetime.datetime(2014,11,30,23,59,59)
startTime=time.mktime(startTime.timetuple())*1000
endTime=time.mktime(endTime.timetuple())*1000

url_db='mongodb://localhost/self'
con=MongoClient(url_db)
db=con.self
col=db.test01
global list_no_results
global list_yes_results
list_no_results=[]
list_yes_results=[]
if exists('./list_ok.log'):
    list_done = [i[:-1] for i in file('./list_ok.log', 'r').readlines()]
else :
    list_done=[]
#www.6wm.cn 1.post 2.get 
def dumpDB(dic,col):
    try:
        col.insert(dic)
    except Exception,e:
        print 'dumpDB',e
    
def parseData(htmls):
    dic={}
    s=BeautifulSoup(htmls)
    list=s.find_all('li')
    dic['id']=list[3].get_text('|').split('|')[1]
    dic['lt']=list[4].get_text('|').split('|')[1]
    dic['type']=list[5].get_text('|').split('|')[1]
    return dic #卡号id, 归属地lt，卡种type  dict

    
def getInfoFromWeb01(cardNumStr):
    #http://www.cha789.com/bank_6228212028001510771.html
    global list_no_results
    global list_yes_results
    url_get='http://www.cha789.com/bank_'+cardNumStr+'.html'
    ip=choice(open('/home/paul/code/formBankDB/ips/ip.list','r').readlines()).strip()
    proxy='http://%s'%(ip)
    opener=urllib2.build_opener(urllib2.ProxyHandler({'http':proxy}))
    urllib2.install_opener(opener)
    try:
        get_1=urlopen(url_get).read()
    except Exception,e:
        print 'getInfoFromWeb01_get1 '
        print e
        #list_no_results.append(cardNumStr)
    if 'cxContext' not in get_1:
        print 'no results 01'
        list_no_results.append(cardNumStr+'\n')
        return False
    else:
        return parseData(get_1)

def doIt(list_id,name,list_no_results,list_yes_results,mylock):
    for i in range(len(list_id)):
        print name+': do it!'
        mylock.acquire()
        id=list_id.pop()
        mylock.release()
        print id
        try:
            dic=getInfoFromWeb01(id)
            if dic:
                dumpDB(dic,col)
                list_yes_results.append(id+'\n')
        except Exception,e:
            print 'getInfoFromWeb01'
            print e
            print list_no_results,'!!!!!!!!!!'
            list_no_results.append(id+'\n') 
        print 'success:',len(list_yes_results)
        print 'erro',len(list_no_results)
    
if __name__=='__main__':
    # dic=getInfoFromWeb01('6217856100007169201')
    # if dic:
        # dic_list.append(dic)
    conn=MongoClient('mongodb://192.168.1.110/')
    mylock = thread.allocate_lock() 
    list_id=[]
    for each in conn['20141205'].withdraw.find({'created_time':{'$gte':startTime,'$lte':endTime}},{'account':1,'_id':0}):
        if each['account'] not in list_id and each['account'] not in list_done:
            list_id.append(each['account'])
    #for i in range(len(list_id)):
        # try:
            # dic=getInfoFromWeb01(each)
            # if dic:
                # dumpDB(dic,col)
                # list_yes_results.append(each+'\n')
        # except Exception,e:
            # print 'getInfoFromWeb01'
            # print e
            # list_no_results.append(each+'\n') #2次都不行，记下
        # print 'success:',len(list_yes_results)
        # print 'erro',len(list_no_results)
    # id=conn['20141126'].withdraw.find_one({},{'account':1,'_id':0})
    # dic_list.append(getInfoFromWeb00(id['account']))
    # if dic_list!=[]:
        # dumpDB(dic_list,col)
    def go(list_id):
        thread.start_new_thread(doIt,(list_id,'A',list_no_results,list_yes_results,mylock))
        thread.start_new_thread(doIt,(list_id,'B',list_no_results,list_yes_results,mylock))
    go(list_id)
    f1=open('./list_ok.log','a')
    f1.writelines(list_yes_results)
    f1.close()
    f2=open('./list_no.log','a')
    f2.writelines(list_no_results)
    f2.close()
    print len(list_no_results)
#00fuction 227 stop;01fuction 761 stop
    
        
