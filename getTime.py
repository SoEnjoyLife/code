import os
import argparse
parser = argparse.ArgumentParser(description="Fuction : creat a time.log ## Author:niuqingshan ## forgod2010@qq.com ## 2014-09-28 11:49:41")
parser.add_argument('-root',help='eg /PROJ/RESEQ/niuqingshan/IndReseq/P2014060251_2tao',required=True)
argv=vars(parser.parse_args())

path=argv['root'].strip()
assert os.path.exists(path)
dic_time={}
dic_key={}
results=[]
samples={}
total_size=0
total=0
#get time for QC
for each in open(path+'/01.QC/nohup.out','r'):
	if 'QC done' in each:
		dic_time['QC']=long(each.split(':')[-1].split('s')[0])
	elif 'Blast NT done' in each:
		dic_time['NT']=long(each.split(':')[-1].split('s')[0])
	elif 'SOAP done' in each:
		dic_time['SOAP']=long(each.split(':')[-1].split('s')[0])

#get time for RESEQ
dic_key={'step2':'BWA and call SNP','step3':'ANNO SNPInDel','step4':'SV','step5':'CNV','step6':'CIRCOS','step10':'STAT'}
for each in open(path+'/02.varDetect/00.bin/time.log','r'):
	line=each.strip().split(' ')
	dic_time[dic_key[line[0]]]=long(line[1])
#get infomation for project
for each in open(path+'/rawData.info','r'):
	if '#' not in each:
		line=each.strip().split('\t')
		samples[line[1]]=float(line[7])
#creat time.log
file=open(path+'/time.log','w')
for each in samples.keys():
	total_size+=samples[each]
results.append(str(len(samples.keys()))+' samples\tTotalSize:'+str(total_size)+'G\n')
for each in dic_time.keys():
	tamp=each+'\t'+str(dic_time[each])+'s\n'
	total+=dic_time[each]
	results.append(tamp)
results.append('total:\t'+str(total/3600)+'h\n')
file.writelines(results)
file.close()