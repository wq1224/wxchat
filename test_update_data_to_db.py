import pdb
import os
import configparser
import datetime
import time
import re
import requests
import json

doc_path = "budda"
user_path = "user"
max_file = 1
new_member_number = 10
#result = ""
store_section = "progress"
store_name = "name"
store_nick_name = "nick_name"
store_last_file = "last_file"
store_last_time = "last_time"
store_first_turn_member_num = "first_turn_member_num"
date_format = "%Y-%m-%d %H:%M:%S"
date_interval = 900



def get_user_id(pinyin):
	user_name = re.sub('\W+','', pinyin)
	return str(int(time.time())) + user_name

def change_record(remark_name, nick_name):
	file = os.path.join(os.getcwd()+os.path.sep+user_path+os.path.sep+nick_name+".conf")
	conf = configparser.ConfigParser()
	if os.path.exists(file) :
		conf.read(file)
		conf.set(store_section, store_name, remark_name)
		conf.set(store_section, store_nick_name, nick_name)
		conf.write(open(file,"w"))
		file_desc = os.path.join(os.getcwd()+os.path.sep+user_path+os.path.sep+remark_name+".conf")
		os.rename(file, file_desc)


github_url = "http://106.14.0.107:8080/angular/getWechatUser?wechatUserId=test"
#data = json.dumps({'name':'test', 'description':'some test repo'}) 
r = requests.get(github_url)
if  r.text.strip():  
	result = r.json()
	print(result["wechatUserId"])
	print(result["jinDu"])
	print(result["updateTime"])
	


