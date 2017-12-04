from wxpy import *
from pycnnum import *
import pdb
import os
import configparser
import datetime
import time
import re

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

bot = Bot(cache_path=False,console_qr=False)
# filepath = os.path.join(os.getcwd()+os.path.sep+path+os.path.sep+file[0:file.rindex(".")])
# bot.file_helper.send_file(filepath+".pdf")
# bot.file_helper.send_file(filepath+".docx")
#my_friend = bot.friends().search('林')[0]
# my_friend2 = bot.friends().search('香瓜子')[0]
# my_friend = bot.file_helper

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

###### remark every people and change files ########
friends = bot.friends()
# for friend in friends :
# 	if friend.remark_name == '':
# 		remark_name = get_user_id(friend.raw["PYQuanPin"])
# 		print("change " + friend.nick_name + " to " + remark_name)
# 		friend.set_remark_name(remark_name)	
# 		time.sleep(30)
for friend in friends :
	change_record(friend.remark_name, friend.nick_name)



# my_friend.send(result)
pdb.set_trace()
