from wxpy import *
from pycnnum import *
import os
import configparser
import datetime
import pdb
import re
import time
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import logging
import hashlib
import requests
import json
from itertools import groupby
logging.basicConfig(level=logging.INFO)
                #filename='wxchat.log'
logging.getLogger('apscheduler').setLevel(logging.INFO)

qrcode_file = "/usr/java/tomcat/apache-tomcat-8.5.16/webapps/scriptures/QR.png"
url = "http://106.14.0.107/scriptures/QR.png"
base_api_url = "http://106.14.0.107:80/angular/"

if os.getenv("QRCODE_FILE") and os.getenv("QRCODE_URL") and os.getenv("API_URL"):
  qrcode_file = os.getenv("QRCODE_FILE")
  url = os.getenv("QRCODE_URL")
  base_api_url = os.getenv("API_URL")

doc_path = "budda"
user_path = "user"
max_file = 1
new_member_number = 10
date_format = "%Y-%m-%d %H:%M:%S"
date_interval = 10

file_store_section = "progress"
file_store_name = "name"
file_store_nick_name = "nick_name"
file_store_last_file = "last_file"
file_store_last_time = "last_time"
file_store_first_turn_member_num = "first_turn_member_num"

store_section = "progress"
store_name = "wechatUserId"
store_nick_name = "userName"
store_last_file = "jinDu"
store_last_time = "updateTime"
store_first_turn_member_num = "groupMember"

md5 = "md5"
sent = False

for file in os.listdir(doc_path):
	if "pdf" in file :
		seq = int(file.split(".")[0])
		if seq > max_file :  
			max_file = seq

# for file in os.listdir(path):
# 	sep = os.path.splitext(file)
# 	if sep[1]=='.pdf':  
# 		result += sep[0] + os.linesep

reply_accept = "您好，{0}，我是灯灯，感谢您关注灯灯哦。试着给我打个招呼吧。"
reply_ask_first = "您好，{0}，我是灯灯，现在我可以提供佛学的讲义给您，目前一共有{1}章内容，您现在想学习第几章？(如需要请回复章节号，如第1章，否则请回复再见，回复“目录”可以查看所有文章目录。"
reply_ask_next = "您好，{0}，我这边显示您已经学完了前{1}章呢，真了不起，目前一共有{2}章内容，您现在想学习第几章？(如需要请回复章节号，如第{2}章，否则请回复再见，回复“目录”可以查看所有文章目录。"
reply_no_need = "您现在不需要的话，那就有需要的时候再找灯灯了哦，灯灯先去服务其它佛友同修了哦！^_^ (如有需要请再次给我打招呼哦)"
reply_no_permission = "您现在还没学到这一章哦，只能学习前{0}章的内容。"

reply_group_first = "大家好，我是灯灯，今天开始我们从头开始学习佛学讲义。下面将分享第1章内容。"
reply_group_continue = "大家好，我是灯灯，今天我们继续学习佛学讲义。下面将分享第{0}章内容。"
#reply_next.format("a","b","c")
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

def list_detail_files():
	files = os.listdir(doc_path)
	files = list( filter( lambda file_name: "pdf" in file_name and "《" in file_name , files ) )
	files.map
	files.sort( key = lambda file_name:int(file_name.split(".")[0]) )
	str = u"目录"
	for file in files:
		str += '\n' + file
	max_file = len(files)
	return str

def filename_match(file_name):
    result = re.search(r"《.*》",file_name)
    if result:
        return result.group()
    else:
        return file_name

def list_files():
    files = os.listdir(doc_path)
    temp = list(filter(lambda file_name : "pdf" in file_name , files))
    temp.sort(key = lambda file_name : int(file_name.split(".")[0]))
    temp = groupby(temp, filename_match)
    str_dic = u"目录"
    for key,group in temp:
        t = list(group)
        if len(t) == 1:
            names = t[0].split(".")
            str_dic += '\n第' + names[0] + "讲 " + names[1].split(" ")[1]
        else:
            start = t[0].split(".")[0]
            end = t[len(t)-1].split(".")[0]
            str_dic += '\n第' + start + "-" + end + "讲 " + key
    return str_dic

def log_to_mail(log_msg,image_file=None):
	try:
		mail = "337569887@qq.com"
		mail_to = "337569887@qq.com;linqifg@163.com"
		passwd = "ddtgzhtuejxpbjig"
		msg = MIMEMultipart('related')
		html_content = "<h3>" + log_msg + "</h3>"
		if image_file:
			fp = open(image_file, 'rb')
			msgImage = MIMEImage(fp.read())
			fp.close()
			msgImage.add_header('Content-Disposition', 'attachment', filename=image_file)
			msgImage.add_header('Content-ID', '<0>')
			msg.attach(msgImage)
			html_content += "<img src=\"cid:0\"/>"
		#msg = EmailMessage()
		#msg.set_content(log_msg)
		msgText = MIMEText(html_content, 'html', 'utf-8')
		msg.attach(msgText)
		msg['Subject'] = log_msg
		msg['From'] = mail
		msg['To'] = mail_to
		s = smtplib.SMTP_SSL("smtp.qq.com",465)
		s.login(mail, passwd)
		#s.send(sender, receiver, msgRoot.as_string())
		s.send_message(msg)
		logging.warning("发送成功")
	except smtplib.SMTPException as e:
	    logging.warning("发送失败")

def kill_process():
	ps_str = os.popen("ps -ef | grep python3").read()
	ps_strs = ps_str.splitlines()
	for each_ps in ps_strs:
		if "test.py" in each_ps:
			ps_str = each_ps
	pid = ps_str.split()[1]
	os.system("kill -9 " + pid)

                                  
def md5sum(filename):
  with open(filename, mode='rb') as f:
    d = hashlib.md5()
    while True:
      buf = f.read(4096) # 128 is smaller than the typical filesystem block
      if not buf:
        break
      d.update(buf)
    return d.hexdigest()

# def studyProgress(remark_name):
# 	file = os.path.join(os.getcwd()+os.path.sep+user_path+os.path.sep+remark_name+".conf")
# 	if not os.path.exists(file):
# 		return 1
# 	else:
# 		conf = configparser.ConfigParser()
# 		conf.read(file)
# 		last_file = int(conf.get(file_store_section, file_store_last_file))
# 		time = conf.get(file_store_section, file_store_last_time)
# 		last_time = datetime.datetime.strptime(time, date_format)
# 		interval = datetime.datetime.now() - last_time
# 		if last_file >= max_file:
# 			return max_file
# 		elif interval.seconds > date_interval:
# 			return last_file + 1
# 		else:
# 			return last_file

# def recordPrgress(remark_name, nick_name, cur_file):
# 	file = os.path.join(os.getcwd()+os.path.sep+user_path+os.path.sep+remark_name+".conf")
# 	conf = configparser.ConfigParser()
# 	if os.path.exists(file) :
# 		conf.read(file)
# 		last_file = int(conf.get(file_store_section, file_store_last_file))
# 		if last_file < cur_file :
# 			conf.set(file_store_section, file_store_last_file, str(cur_file))
# 			conf.set(file_store_section, file_store_last_time, datetime.datetime.now().strftime(date_format))
# 	else:
# 		conf.add_section(file_store_section)
# 		conf.set(file_store_section, file_store_name, remark_name)
# 		conf.set(file_store_section, file_store_nick_name, nick_name)
# 		conf.set(file_store_section, file_store_last_file, str(cur_file))
# 		conf.set(file_store_section, file_store_last_time, datetime.datetime.now().strftime(date_format))
# 	conf.write(open(file,"w"))

# def studyProgressForGroup(name, cur_member):
# 	file = os.path.join(os.getcwd()+os.path.sep+user_path+os.path.sep+name+".conf")
# 	if not os.path.exists(file):
# 		return 1
# 	else:
# 		conf = configparser.ConfigParser()
# 		conf.read(file)
# 		last_file = int(conf.get(file_store_section, file_store_last_file))
# 		first_turn_member_num = int(conf.get(file_store_section, file_store_first_turn_member_num))
# 		if cur_member - first_turn_member_num >= new_member_number:
# 			return 1
# 		elif last_file >= max_file:
# 			return 1
# 		else:
# 		 	return last_file + 1

# def recordPrgressForGroup(name, cur_file, cur_member):
# 	file = os.path.join(os.getcwd()+os.path.sep+user_path+os.path.sep+name+".conf")
# 	conf = configparser.ConfigParser()
# 	if os.path.exists(file) :
# 		conf.read(file)
# 		conf.set(file_store_section, file_store_last_file, str(cur_file))
# 		conf.set(file_store_section, file_store_last_time, datetime.datetime.now().strftime(date_format))
# 		if cur_file == 1 :
# 			conf.set(file_store_section, file_store_first_turn_member_num, str(cur_member))		
# 	else:
# 		conf.add_section(file_store_section)
# 		conf.set(file_store_section, file_store_name, name)
# 		conf.set(file_store_section, file_store_last_file, str(cur_file))
# 		conf.set(file_store_section, file_store_last_time, datetime.datetime.now().strftime(date_format))
# 		conf.set(file_store_section, file_store_first_turn_member_num, str(cur_member))
# 	conf.write(open(file,"w"))

def studyProgress(remark_name):
	result = get_user_info(remark_name)
	if not result:
		return 1
	else:
		last_file = int(result[store_last_file])
		time = result[store_last_time]
		last_time = datetime.datetime.strptime(time, date_format)
		interval = datetime.datetime.now() - last_time
		if last_file >= max_file:
			return max_file
		# elif interval.seconds > date_interval:
		# 	return last_file + 1
		else:
			return last_file

def recordPrgress(remark_name, nick_name, cur_file):
	result = get_user_info(remark_name)
	if result:
		last_file = int(result[store_last_file])
		if last_file < cur_file :
			result[store_last_file] = str(cur_file)
			update_user_info(result)
	else:
		result = {store_name: remark_name, store_nick_name: nick_name, store_last_file: str(cur_file) }
		insert_user_info(result)

def studyProgressForGroup(name, cur_member):
	result = get_user_info(name)
	if not result:
		return 1
	else:
		last_file = int(result[store_last_file])
		first_turn_member_num = int(result[store_first_turn_member_num])
		if cur_member - first_turn_member_num >= new_member_number:
			return 1
		elif last_file >= max_file:
			return 1
		else:
		 	return last_file + 1

def recordPrgressForGroup(name, cur_file, cur_member):
	result = get_user_info(name)
	if result :
		result[store_last_file] = str(cur_file)
		if cur_file == 1 :
			result[store_first_turn_member_num] = str(cur_member)
		update_user_info(result)	
	else:
		result = {
			store_name: name, 
			store_nick_name: name,
			store_last_file: str(cur_file),
			store_first_turn_member_num: str(cur_member)
		}
		insert_user_info(result)

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

def get_user_remark_name(pinyin):
	user_name = re.sub('\W+','', pinyin)
	return str(int(time.time())) + user_name
	
def isSayHello(msg):
	return "Hi" in msg or "Hello" in msg or "你好" in msg or "您好" in msg  or "在吗" in msg or "在嘛" in msg or "在？" in msg

def isFirstNeed(msg):
	return ("是" in msg or "需要" in msg) and ("不" not in msg)

def isDictionary(msg):
	return ("目录" in msg)

def isSayBye(msg):
	return "再见" in msg or "Bye" in msg or "拜拜" in msg or "bye" in msg

def isNextNumber(msg):
	msg_number = msg.strip()
	m = re.search("第(.*)(章|讲)", msg_number)
	if (m is not None):
		msg_number = m.group(1)
	return str2num(msg_number)

def str2num(str):
	if cn2num(str):
		return cn2num(str)
	try:
		return int(str)
	except ValueError:
		return 0

try:
	log_to_mail("system start now")
	sched = BackgroundScheduler()
	@sched.scheduled_job('interval', id="qrcode_check", seconds=60)
	def qrcode_check():
		global md5
		global sent
		if os.path.exists(qrcode_file):
			#temp_md5 = md5sum(qrcode_file)
			#if temp_md5 != md5:
			if not sent:
				log_to_mail("Dengdeng need login, please scan qr code <a>" + url + "</a>")
				sent = True
				#md5 = temp_md5

	sched.start()
	bot = Bot(cache_path=True,console_qr=False, qr_path=qrcode_file)
	if os.path.exists(qrcode_file):
		os.remove(qrcode_file)
	sched.remove_job("qrcode_check")
	# filepath = os.path.join(os.getcwd()+os.path.sep+path+os.path.sep+file[0:file.rindex(".")])
	# bot.file_helper.send_file(filepath+".pdf")
	# bot.file_helper.send_file(filepath+".docx")
	log_person = bot.friends().search('wangqiong')[0]
	log_person.send("dengdeng started")
	# my_friend2 = bot.friends().search('香瓜子')[0]
	# my_friend = bot.file_helper

	# my_friend.send(result)

	# 自动接受新的好友请求
	@bot.register(msg_types=FRIENDS)
	def auto_accept_friends(msg):
	    # 接受好友请求
	    new_friend = msg.card.accept()
	    # 给好友备注 时间戳+昵称拼音(过滤除字母数字外的字符)
	    remark_name = get_user_remark_name(new_friend.raw["PYQuanPin"])
	    logging.warning("accepted new friend " + remark_name)
	    new_friend.set_remark_name(remark_name)
	    # 向新的好友发送消息
	    new_friend.send(reply_accept.format(new_friend.nick_name))
	    logging.warning("sent hello to new friend " + remark_name)

	# 回复 my_friend 的消息 (优先匹配后注册的函数!)
	#@bot.register(my_friend)
	@bot.register(Friend, TEXT)
	def reply_my_friend(msg):
		msg_text = msg.text.strip()
		user = msg.sender.remark_name
		logging.warning("ready to reply to friend " + user)
		# 请求目录
		if isDictionary(msg_text):
			dictionary_text = list_files()
			return dictionary_text
		# 请求文章
		next_number = isNextNumber(msg_text)
		if next_number !=0 :
			msg.sender.send_file(get_article(next_number))
			logging.warning("replied " + str(next_number) + " article to " + user)
			progress = studyProgress(user)
			if (progress < next_number):
				recordPrgress(user, msg.sender.nick_name, next_number)
			return
		# 再见
		if isSayBye(msg_text):
			return reply_no_need
		# 其他情况
		progress = studyProgress(user)
		if 1 == progress:
			return reply_ask_first.format( msg.sender.nick_name, max_file )
		else:
			return reply_ask_next.format( msg.sender.nick_name, progress, max_file )


	#sched = BackgroundScheduler()

	@sched.scheduled_job('cron', day_of_week='mon-sun', hour=20)
	def scheduled_job():
		logging.warning("start scheduled_job to send articles to group")
		groups = bot.groups()
		logging.warning("get groups name over")
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
			logging.warning("send " + str(progress) + " article to group " + group_name)

	# @sched.scheduled_job('interval', minutes=3)
	# def scheduled_job_test():
	# 	logging.warning("start scheduled_job to send articles to group")
	# 	group = bot.groups().search('测试灯灯')[0]
	# 	logging.warning("get groups name over")
	# 	current_members = len(group.members)
	# 	group_name = group.name
	# 	progress = studyProgressForGroup(group_name,current_members)
	# 	if progress == 1:
	# 		group.send(reply_group_first)
	# 	else:
	# 		group.send(reply_group_continue.format(progress))
	# 	group.send_file(get_article(progress))
	# 	recordPrgressForGroup(group_name, progress, current_members)
	# 	logging.warning("send " + str(progress) + " article to group " + group_name)	


	@sched.scheduled_job('interval', minutes=60)
	def heart_beat():
		try:
			logging.warning("start scheduled_job to send msg to writer for heartbeat")
			log_person.send("dengdeng works fine")
			logging.warning("sent to writer over")
		except ResponseError as r:
			logging.warning("dengdeng encounter ResponseError when heart beat")
			log_to_mail("dengdeng encounter ResponseError when heart beat")
			kill_process()
			sys.exit();
		except Exception as e:
			logging.warning("dengdeng encounter Exception when heart beat")
			log_to_mail("dengdeng encounter Exception when heart beat")
			kill_process()
			sys.exit();

	# @sched.scheduled_job('interval', seconds=20)
	# def heart_beat_alive():
	# 	logging.warning("alive:" + str(bot.alive))
	# 	if not bot.alive:
	# 		logging.warning("not alive, send email")
	# 		log_to_mail("dengdeng not alive now")
	# 		sys.exit();
	# 	else:
	# 		logging.warning("alive, continue")

	bot.join()

except ResponseError as r:
	logging.warning("encounter ResponseError")
	log_to_mail("dengdeng encounter ResponseError")
	sys.exit();
except Exception as e:
	print(e)
	logging.warning("encounter Exception")
	log_to_mail("dengdeng encounter Exception")
	sys.exit();

#embed()

# 回复 my_friend 的消息 (优先匹配后注册的函数!)
# @bot.register(my_friend2)
# def reply_my_friend(msg):
# 	if msg.text:
# 		msg_text = msg.text.strip()
# 		for file in os.listdir(path):
# 			if msg_text == file.split(".")[0]:  
# 				msg.sender.send_file(path+"/"+file)
# 	else 
# 		return "您输入的内容无法识别"

#test
# def reply_my_friend(msg,user):
# 	msg_text = msg
# 	#回复打招呼
# 	if isSayHello(msg_text):
# 		progress = studyProgress(user)
# 		if 1 == progress:
# 			return reply_first.format(user)
# 		else:
# 			return reply_next.format(user,progress-1, progress)
# 	#回复第一章(只有第一章的回复为是,否)
# 	if isFirstNeed(msg_text):
# 		recordPrgress(user, 1)
# 		return get_article(1)
# 	#回复后续章
# 	next_number = isNextNumber(msg_text)
# 	if next_number !=0 :
# 		progress = studyProgress(user)
# 		if (progress >= next_number):
# 			recordPrgress(user,next_number)
# 			return get_article(next_number)
			
# 	return reply_no_need

#print(reply_my_friend("您好","wangqiong"))
#print(reply_my_friend("是","wangqiong"))
#print(reply_my_friend("第4章","wangqiong"))

####### group test #########
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
