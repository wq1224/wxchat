from wxpy import *
from pycnnum import *
import pdb
import os
import configparser
import datetime
import time
import re
from apscheduler.schedulers.background import BackgroundScheduler

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

#pdb.set_trace()
bot = Bot(cache_path=False,console_qr=False)
# filepath = os.path.join(os.getcwd()+os.path.sep+path+os.path.sep+file[0:file.rindex(".")])
# bot.file_helper.send_file(filepath+".pdf")
# bot.file_helper.send_file(filepath+".docx")
#my_friend = bot.friends().search('灯灯')[0]
my_friend2 = bot.friends().search('林显春')[0]
my_friend = bot.file_helper

def get_article(seq=1):
	for file in os.listdir(doc_path):
		if "pdf" in file :
			file_seq = int(file.split(".")[0])
			if seq == file_seq:
				filepath = os.path.join(os.getcwd()+os.path.sep+doc_path+os.path.sep+file[0:file.rindex(".")])
				#msg.sender.send_file(filepath+".pdf")
				#msg.sender.send_file(filepath+".docx")
				return filepath+".pdf"
	return
#@bot.register(my_friend, TEXT)
def reply_my_friend(msg):
	msg.sender.send_file(get_article(1))

# my_friend.send(result)
#bot.logout()
embed()
