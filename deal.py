#!/usr/bin/python
# -*- coding: utf-8 -*-  

import os
import sys
import time

start_time=int(time.time())
time_array=time.localtime(start_time)
time_style=time.strftime("%Y-%m-%d %H:%M:%S",time_array)

print "START:%s"%time_style

os.system('mkdir -p tmp_data')
os.system('rm -f tmp_data/*.txt')
f_src=open('./datas.txt')
print "Get Searched Data Success!"

data_str=f_src.read()
data_r=data_str.strip('\n').split('\n')
datas=[]
datas=[line.strip('\r') for line in data_r]
ser_data='|'.join(datas)
print ser_data
print "Begin to Collect Data"
os.system('grep -E "%s" ali_data_get.log > ./tmp_data/Get.txt'%ser_data)
os.system('grep -E "%s" ali_change_*.log > ./tmp_data/Chg.txt'%ser_data) 
os.system('grep -E "%s" cms_change_*.log > ./tmp_data/CMS.txt'%ser_data) 
os.system('grep -E "%s" pass_worklist.log > ./tmp_data/Pass.txt'%ser_data) 
os.system('grep -E "%s" unprocess_worklist.log > ./tmp_data/Unpro.txt'%ser_data) 
os.system('grep -E "%s" consist_worklist.log > ./tmp_data/Con.txt'%ser_data) 
os.system('grep -E "%s" metaq_resent.log > ./tmp_data/Qresnd.txt'%ser_data) 
os.system('grep -E "%s" cms_repeat.log > ./tmp_data/Rept.txt'%ser_data)
print "Collection is over."

print "Preparing Needed Resources"
opponent={}
opponent['get']={}
opponent['get']['f_in']=open('./tmp_data/Get.txt','r')
opponent['get']['f_out1']=open('./tmp_data/get_inPriWL.txt','w')
opponent['get']['f_out2']=open('./tmp_data/get_inMongo.txt','w')
opponent['get']['f_out3']=open('./tmp_data/get_notRciv.txt','w')
opponent['get']['f_else']=open('./tmp_data/get_else.txt','w')
opponent['get']['info1']="ali metaq data add to priority worklist success!"
opponent['get']['info2']="get ali data,add to mongo success."
opponent['chg']={}
opponent['chg']['f_in']=open('./tmp_data/Chg.txt','r')
opponent['chg']['f_out1']=open('./tmp_data/chg_inWL.txt','w')
opponent['chg']['f_out2']=open('./tmp_data/chg_cIn.txt','w')
opponent['chg']['f_else']=open('./tmp_data/chg_else.txt','w')
opponent['chg']['info1']="Add worklist success"
opponent['chg']['info2']="Ali data checkin success"
opponent['cms']={}
opponent['cms']['f_in']=open('./tmp_data/CMS.txt','r')
opponent['cms']['f_out1']=open('./tmp_data/cms_inWL.txt','w')
opponent['cms']['f_out2']=open('./tmp_data/cms_back.txt','w')
opponent['cms']['f_else']=open('./tmp_data/cms_else.txt','w')
opponent['cms']['info1']="Add worklist success"
opponent['cms']['info2']="Send back gaode data into metaq success"
opponent['passwl']={}
opponent['passwl']['f_in']=open('./tmp_data/Pass.txt','r')
opponent['passwl']['f_out1']=open('./tmp_data/pass_inMongo.txt','w')
opponent['passwl']['f_out2']=open('./tmp_data/pass_back.txt','w')
opponent['passwl']['f_else']=open('./tmp_data/pass_else.txt','w')
opponent['passwl']['info1']="visit put_cms_modify_data_2_metaq service failed and input to mongo success"
opponent['passwl']['info2']="Send back gaode data into metaq success"
opponent['unpro']={}
opponent['unpro']['f_in']=open('./tmp_data/Unpro.txt','r')
opponent['unpro']['f_out1']=open('./tmp_data/unpro_inMongo.txt','w')
opponent['unpro']['f_out2']=open('./tmp_data/unpro_back.txt','w')
opponent['unpro']['f_else']=open('./tmp_data/unpro_else.txt','w')
opponent['unpro']['info1']="visit put_cms_modify_data_2_metaq service failed and input to mongo success"
opponent['unpro']['info2']="Send back gaode data into metaq success"
opponent['consist']={}
opponent['consist']['f_in']=open('./tmp_data/Con.txt','r')
opponent['consist']['f_out1']=open('./tmp_data/con_inWL.txt','w')
opponent['consist']['f_out2']=open('./tmp_data/con_back.txt','w')
opponent['consist']['f_else']=open('./tmp_data/con_else.txt','w')
opponent['consist']['info1']="Add worklist success"
opponent['consist']['info2']="Send back gaode data into metaq success"
opponent['repeat']={}
opponent['repeat']['f_in']=open('./tmp_data/Rept.txt','r')
opponent['repeat']['f_out1']=open('./tmp_data/rept_fail.txt','w')
opponent['repeat']['f_out2']=open('./tmp_data/rept_success.txt','w')
opponent['repeat']['f_else']=open('./tmp_data/rept_else.txt','w')
opponent['repeat']['info1']="put metaq fail"
opponent['repeat']['info2']="Send back to metaq success."
opponent['qresend']={}
opponent['qresend']['f_in']=open('./tmp_data/Qresnd.txt','r')
opponent['qresend']['f_out1']=open('./tmp_data/qresnd_inWL.txt','w')
opponent['qresend']['f_out2']=open('./tmp_data/qresnd_back.txt','w')
opponent['qresend']['f_else']=open('./tmp_data/qresnd_else.txt','w')
opponent['qresend']['info1']="Add worklist success"
opponent['qresend']['info2']="resend info to metaq success."

print "Start to classify the datas"
for key in opponent:
    process=[]
    unprocess=[]
    poiid_dic={}
    poiid_pass=[]
    for line in opponent[key]['f_in'].readlines():
        pos_id=line.find('db_id')
        if pos_id<0:
            continue
        db_id=line[pos_id+6:pos_id+14]
        db_id.strip(' ')

        if key=='get':
            if db_id in datas:
                datas.remove(db_id)
        pos_poiid=line.find('poiid')
        if not db_id in unprocess:
            unprocess.append(db_id)
            if pos_poiid<0:
                pass
            else:
                poiid_dic[db_id]=line[pos_poiid+6:pos_poiid+16]

        pos_info=line.find(opponent[key]['info1'])
        if pos_info<0:
            pass
        else:
            opponent[key]['f_out1'].write("db_id:%s  "%db_id) 
            opponent[key]['f_out1'].write(line)
            unprocess.remove(db_id)
            process.append(db_id)
            continue

        pos_info=line.find(opponent[key]['info2'])
        if pos_info<0:
            if db_id in process:
                unprocess.remove(db_id)
        else:
            opponent[key]['f_out2'].write("db_id:%s "%db_id)
            opponent[key]['f_out2'].write(line)
            unprocess.remove(db_id)
            process.append(db_id)
            poiid_pass.append(db_id)
            continue
    for id in unprocess:
        opponent[key]['f_else'].write("db_id:%s\n"%id)
    if key=='get':
        for id in datas:
            opponent[key]['f_out3'].write("db_id:%s\n"%id)
    if key=='cms':
        f_out_pair=open('tmp_data/cms_pair.txt','w')
        for id in poiid_pass:
            f_out_pair.write("db_id:%s  "%id)
            f_out_pair.write("poiid:%s\n"%poiid_dic[id])
            
print "The Procedure is Over!"

end_time=int(time.time())
time_array=time.localtime(end_time)
time_style=time.strftime("%Y-%m-%d %H:%M:%S",time_array)

print "END:%s"%time_style
