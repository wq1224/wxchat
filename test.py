from wxpy import *
from pycnnum import *
import os
import configparser
import datetime

doc_path = "budda"
user_path = "user"
max_file = 1
#result = ""
store_section = "progress"
store_name = "name"
store_last_file = "last_file"
store_last_time = "last_time"
date_format = "%Y-%m-%d %H:%M:%S"
date_interval = 60


for file in os.listdir(doc_path):
	if "pdf" in file :
		seq = int(file.split(".")[0])
		if seq > max_file :  
			max_file = seq

# for file in os.listdir(path):
# 	sep = os.path.splitext(file)
# 	if sep[1]=='.pdf':  
# 		result += sep[0] + os.linesep

reply_accept = "您好，{0}，我是小胖胖，感谢您关注小胖胖哦。试着给我打个招呼吧。"
reply_first = "您好，{0}，我是小胖胖，现在我可以提供佛学的讲义给您，请问您是否需要开始学习？（回复“是”或“需要”可以得到第一章讲义)"
reply_next = "您好，{0}，我这边显示您已经学完了前{1}章呢，真了不起，您已经可以开始学习第{2}章了哟，您现在想学习第几章？"
reply_no_need = "您现在不需要的话，那就有需要的时候再找小胖胖了哦，小胖胖先去服务其它佛友同修了哦！^_^"
#reply_next.format("a","b","c")

def isSayHello(msg):
	return "Hi" in msg or "Hello" in msg or "你好" in msg or "您好" in msg  or "在吗" in msg or "在嘛" in msg or "在？" in msg

def isFirstNeed(msg):
	return ("是" in msg or "需要" in msg) and ("不" not in msg)

def isNextNumber(msg):
	msg_number = msg.strip()
	if ("第" in msg):
		msg_number = msg[1:-1].strip()
	return str2num(msg_number)

def str2num(str):
	if not cn2num(str):
		return cn2num(str)
	try:
		return int(str)
	except ValueError:
		return 0

def studyProgress(name):
	file = os.path.join(os.getcwd()+os.path.sep+user_path+os.path.sep+name+"conf")
	if not os.path.exists(file):
		return 1
	else:
		conf = configparser.ConfigParser()
		conf.read(file)
		last_file = conf.get(store_section, store_last_file)
		time = conf.get(store_section, store_last_time)
		last_time = datetime.datetime.strptime(time, date_format)
		interval = datetime.datetime.now - last_time
		if interval.seconds > date_interval:
			return last_file + 1
		else:
			return last_file

def recordPrgress(name, cur_file):
	file = os.path.join(os.getcwd()+os.path.sep+user_path+os.path.sep+name+"conf")
	conf = ConfigParser.ConfigParser()
	conf.add_section(store_section)
	conf.set(store_section, store_name, datetime.datetime.now)
	conf.set(store_section, store_last_file, cur_file)
	conf.set(store_section, store_last_time, datetime.datetime.now)
	conf.write(open(file))

def get_article(seq=1):
	file_seq = int(file.split(".")[0])
	for file in os.listdir(path):
		if seq == file_seq:
			filepath = os.path.join(os.getcwd()+os.path.sep+doc_path+os.path.sep+file[0:file.rindex(".")])
			#msg.sender.send_file(filepath+".pdf")
			#msg.sender.send_file(filepath+".docx")
			return filepath+".pdf"
	return

bot = Bot(cache_path=True,console_qr=True)
# filepath = os.path.join(os.getcwd()+os.path.sep+path+os.path.sep+file[0:file.rindex(".")])
# bot.file_helper.send_file(filepath+".pdf")
# bot.file_helper.send_file(filepath+".docx")

# my_friend = bot.friends().search("林显春")[0]
# my_friend2 = bot.friends().search('香瓜子')[0]
my_friend = bot.file_helper

my_friend.send(result)

# 自动接受新的好友请求
@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    # 接受好友请求
    new_friend = msg.card.accept()
    # 向新的好友发送消息
    new_friend.send(reply_accept.format(mgs.sender))

# 回复 my_friend 的消息 (优先匹配后注册的函数!)
@bot.register(my_friend)
def reply_my_friend(msg):
	if msg.text:
		msg_text = msg.text.strip()
		user = msg.sender
		#回复打招呼
		if isSayHello(msg_text):
			progress = studyProgress(user)
			if 1 == progress:
				return reply_first.format(user)
			else:
				return reply_next.format(user,progress, progress+1)
		#回复第一章(只有第一章的回复为是,否)
		if isFirstNeed(msg_text):
			msg.sender.send_file(get_article(1))
			return
		#回复后续章
		next_number = isNextNumber(msg_text)
		if number !=0 :
			progress = studyProgress(user)
			if (progress >= next_number):
				msg.sender.send_file(get_article(next_number))
				return
	return reply_no_need

# # 回复 my_friend 的消息 (优先匹配后注册的函数!)
# @bot.register(my_friend2)
# def reply_my_friend(msg):
# 	if msg.text:
# 		msg_text = msg.text.strip()
# 		for file in os.listdir(path):
# 			if msg_text == file.split(".")[0]:  
# 				msg.sender.send_file(path+"/"+file)
# 	else 
# 		return "您输入的内容无法识别"
embed()