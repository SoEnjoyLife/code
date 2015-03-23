from urllib2 import urlopen
from bs4 import BeautifulSoup
import re

#htmls=[]
ips=[]
def parseIP(html):
    ips=[]
    ports=[]
    servers=[]
    s=BeautifulSoup(html)
    for i in s.find_all('td',text=re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')):
        ips.append(i.string)
    for i in s.find_all('td',text=re.compile('^\d{2,4}$')):
        ports.append(i.string)
    for i,j in zip(ips,ports):
        servers.append(i+':'+j+'\n')
    return servers

for i in range(1,5):
    url='http://www.kuaidaili.com/proxylist/'+str(i)+'/'
    tamp=[]
    try:
        html=urlopen(url).read()
        tamp=parseIP(html)
    except Exception,e:
        print e
        print 'end in page:'+url+'\n'
        break
    if tamp!=[]:
        #global ips
        ips+=tamp
if ips!=[]:
    f=open('/home/paul/code/formBankDB/ips/ip.list','w')
    f.writelines(ips)
#s.find('td',text=re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')).string
