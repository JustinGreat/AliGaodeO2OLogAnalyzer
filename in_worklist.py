#encoding=gb18030
import os
import sys
reload(sys)
sys.setdefaultencoding("gb18030")
import urllib2
import time
import json
import traceback
sys.path.append("/home/carrey/common_utility")
from common import getDate


str_time = time.strftime('%Y_%m_%d',time.localtime(time.time()))
ss_time = time.strftime('%Y%m%d000000',time.localtime(time.time()))
ifile = "./ali/ALIO2O_data"
ofile = "./inworklist/in_worklist_%s"%str_time
ofile2= "./inworklist/in_worklist_3days%s"%str_time
#os.system('grep  "\"status\": \"0\"" %s | grep "\"worklist\": \"1\"" > %s'%(ifile,ofile))
#os.system('grep  ""status": "0"" %s > %s'%(ifile,ofile))
fout = open(ofile,"w")
fout_3days = open(ofile2,"w")
lines = [line.strip("\n").split("\t") for line in file(ifile)]
for line in lines:
    try:	
    	data_json = json.loads(line[-1])
    except:
    	continue
    status = data_json.get("status","")
    worklist = data_json.get("worklist","")
    cms = data_json.get("status_cms","")
    if worklist == "1":
        fout.write(line[-1]+"\n")
        dtime = data_json.get("time","0").replace("-","").replace(" ","").replace(":","")
        if long(dtime) +2000000 < long(ss_time):
            fout_3days.write(line[-1]+"\n")
fout.close()

