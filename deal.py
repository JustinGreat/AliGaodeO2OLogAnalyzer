#!/usr/bin/python

import os
import sys


f_src=open('./datas.txt')

data_str=f_src.read()
data_r=data_str.split('\n')
datas=[]
datas=[line.strip('\r') for line in data_r]
ser_data='|'.join(datas)

os.system('grep -E "%s" ali_change_*.log > ./tmp_data/Chg.txt'%ser_data) 
os.system('grep -E "%s" cms_change_*.log > ./tmp_data/CMS.txt'%ser_data) 
os.system('grep -E "%s" pass_worklist.log > ./tmp_data/Pass.txt'%ser_data) 
os.system('grep -E "%s" unprocess_worklist.log > ./tmp_data/Unpro.txt'%ser_data) 
os.system('grep -E "%s" consist_worklist.log > ./tmp_data/Con.txt'%ser_data) 
os.system('grep -E "%s" metaq_resent.log > ./tmp_data/Qresnd.txt'%ser_data) 

opponent={}
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
opponent['qresend']={}
opponent['qresend']['f_in']=open('./tmp_data/Qresnd.txt','r')
opponent['qresend']['f_out1']=open('./tmp_data/qresnd_inWL.txt','w')
opponent['qresend']['f_out2']=open('./tmp_data/qresnd_back.txt','w')
opponent['qresend']['f_else']=open('./tmp_data/qresnd_else.txt','w')
opponent['qresend']['info1']="Add worklist success"
opponent['qresend']['info2']="resend info to metaq success."

for key in opponent:
    process=[]
    unprocess=[]
    for line in opponent[key]['f_in'].readlines():
        pos_id=line.find('db_id')
        if pos_id<0:
            continue
        db_id=line[pos_id+6:pos_id+14]
        if not db_id in unprocess:
            unprocess.append(db_id)
     
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
            continue
    for id in unprocess:
        opponent[key]['f_else'].write("db_id:%s\n"%id)
    
