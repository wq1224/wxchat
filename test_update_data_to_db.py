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

base_api_url = "http://106.14.0.107:80/angular/"

def get_user_info(user_remark_name):
	result = requests.get(base_api_url + "getWechatUser?wechatUserId=" + user_remark_name)
	if  result.text.strip(): 
		return result.json()
	else:
		return

def update_user_info(user_info):
	change_user_info(user_info,"u")

def insert_user_info(user_info):
	change_user_info(user_info, "i")

def change_user_info(user_info,sql_type):
	url = base_api_url + "updateUserDB?wechatUserId=" + user_info[store_name]
	url = url + "&type=" + sql_type
	keys = user_info.keys()
	if store_nick_name in keys:
		url = url + "&userName=" + user_info[store_nick_name]
	if store_first_turn_member_num in keys and user_info[store_first_turn_member_num] != 0:
		url = url + "&groupMember=" + str(user_info[store_first_turn_member_num])
	if store_last_file in keys:
		url = url + "&jingWenJinDu=" + str(user_info[store_last_file])
	result = requests.get(url)

#data = json.dumps({'name':'test', 'description':'some test repo'}) 
for file in os.listdir(user_path):
	if "conf" in file :
		conf = configparser.ConfigParser()
		conf.read(os.path.join(os.getcwd()+os.path.sep+user_path+os.path.sep+file))
		values = dict(conf.items(store_section))
		result = {}
		for key in values.keys():
			result[key] = values[key]
		username = os.path.splitext(file)[0]
		r = get_user_info(username)
		if  r:  
			update_user_info(result)
		else:
			insert_user_info(result)
	


