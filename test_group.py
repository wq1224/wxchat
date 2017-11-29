from wxpy import *
from pycnnum import *
import os
import configparser
import datetime
import pdb
import re

doc_path = "budda"
user_path = "user"
max_file = 1
#define the number of the new members in the group to trigger new turn
new_member_number = 10
#result = ""
store_section = "progress"
store_name = "name"
store_last_file = "last_file"
store_last_time = "last_time"
store_first_turn_member_num = "first_turn_member_num"
date_format = "%Y-%m-%d %H:%M:%S"
date_interval = 900

for file in os.listdir(doc_path):
	if "pdf" in file :
		seq = int(file.split(".")[0])
		if seq > max_file :  
			max_file = seq

# for file in os.listdir(path):
# 	sep = os.path.splitext(file)
# 	if sep[1]=='.pdf':  
# 		result += sep[0] + os.linesep

#reply_next.format("a","b","c")
reply_group_first = "大家好，我是灯灯，今天开始我们从头开始学习佛学讲义。下面将分享第1章内容。"
reply_group_continue = "大家好，我是灯灯，今天我们继续学习佛学讲义。下面将分享第{0}章内容。"

def studyProgressForGroup(name, cur_member):
	file = os.path.join(os.getcwd()+os.path.sep+user_path+os.path.sep+name+".conf")
	if not os.path.exists(file):
		return 1
	else:
		conf = configparser.ConfigParser()
		conf.read(file)
		last_file = int(conf.get(store_section, store_last_file))
		first_turn_member_num = int(conf.get(store_section, store_first_turn_member_num))
		if cur_member - first_turn_member_num >= new_member_number:
			return 1
		elif last_file >= max_file:
			return 1
		else:
		 	return last_file + 1

def recordPrgressForGroup(name, cur_file, cur_member):
	file = os.path.join(os.getcwd()+os.path.sep+user_path+os.path.sep+name+".conf")
	conf = configparser.ConfigParser()
	if os.path.exists(file) :
		conf.read(file)
		conf.set(store_section, store_last_file, str(cur_file))
		conf.set(store_section, store_last_time, datetime.datetime.now().strftime(date_format))
		if cur_file == 1 :
			conf.set(store_section, store_first_turn_member_num, str(cur_member))		
	else:
		conf.add_section(store_section)
		conf.set(store_section, store_name, name)
		conf.set(store_section, store_last_file, str(cur_file))
		conf.set(store_section, store_last_time, datetime.datetime.now().strftime(date_format))
		conf.set(store_section, store_first_turn_member_num, str(cur_member))
	conf.write(open(file,"w"))

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


bot = Bot(cache_path=False,console_qr=False)
# filepath = os.path.join(os.getcwd()+os.path.sep+path+os.path.sep+file[0:file.rindex(".")])
# bot.file_helper.send_file(filepath+".pdf")
# bot.file_helper.send_file(filepath+".docx")
my_friend = bot.friends().search('林显春')[0]
# my_friend2 = bot.friends().search('香瓜子')[0]
# my_friend = bot.file_helper
# my_friend.send(result)

#group = bot.groups().search('林显春（电信）、linky')


from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()

@sched.scheduled_job('interval', minutes=5)
def timed_job():
	print("scheduler erery 5 min job start")	


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=18)
def scheduled_job():
	print("scheduler job start")
	groups = bot.groups().search('林,王琼,linky')
	for group in groups :
		current_members = len(group.members)
		group_name = group.name
		progress = studyProgressForGroup(group_name,current_members)
		if progress == 1:
			group.send(reply_group_first)
		else:
			group.send(reply_group_continue.format(progress))
		group.send_file(get_article(progress))
		recordPrgressForGroup(group_name, progress, current_members)	

sched.start()

print ("this is main")
#print(group)
have_asked = {}
# 回复 my_friend 的消息 (优先匹配后注册的函数!)
@bot.register(my_friend)
def reply_my_friend(msg):
	msg.sender.send_file(get_article(1))

bot.join()

# def timed_job(group_num, group):
# 	current_members = group_num
# 	progress = studyProgressForGroup(group,current_members)
# 	if progress == 1:
# 		print(reply_group_first)
# 	else:
# 		print(reply_group_continue.format(progress))
# 	recordPrgressForGroup(group, progress, current_members)

# timed_job(2, "group1")
# timed_job(2, "group1")
# timed_job(2, "group1")
# timed_job(2, "group1")
# timed_job(2, "group2")
# timed_job(2, "group1")
# timed_job(2, "group2")
# timed_job(12, "group1")
# timed_job(11, "group2")
# timed_job(13, "group2")

