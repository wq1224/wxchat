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
logging.basicConfig(level=logging.INFO)
                #filename='wxchat.log'
logging.getLogger('apscheduler').setLevel(logging.INFO)

doc_path = "budda"
user_path = "user"
max_file = 1
new_member_number = 10
qrcode_file = "QR.png"
#result = ""
store_section = "progress"
store_name = "name"
store_nick_name = "nick_name"
store_last_file = "last_file"
store_last_time = "last_time"
store_first_turn_member_num = "first_turn_member_num"
date_format = "%Y-%m-%d %H:%M:%S"
date_interval = 900
md5 = "md5"

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
reply_ask_first = "您好，{0}，我是灯灯，现在我可以提供佛学的讲义给您，请问您是否需要开始学习？(如需要请回复是或者需要，否则请回复任意其他内容)"
reply_ask_next = "您好，{0}，我这边显示您已经学完了前{1}章呢，真了不起，您已经可以开始学习第{2}章了哟，您现在想学习第几章？(如需要请回复章节号，如第{2}章，否则请回复任意其他内容)"
reply_no_need = "您现在不需要的话，那就有需要的时候再找灯灯了哦，灯灯先去服务其它佛友同修了哦！^_^ (如有需要请再次给我打招呼哦)"
reply_no_permission = "您现在还没学到这一章哦，只能学习前{0}章的内容。"

reply_group_first = "大家好，我是灯灯，今天开始我们从头开始学习佛学讲义。下面将分享第1章内容。"
reply_group_continue = "大家好，我是灯灯，今天我们继续学习佛学讲义。下面将分享第{0}章内容。"
#reply_next.format("a","b","c")

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

def get_user_remark_name(pinyin):
	user_name = re.sub('\W+','', pinyin)
	return str(int(time.time())) + user_name
	
def isSayHello(msg):
	return "Hi" in msg or "Hello" in msg or "你好" in msg or "您好" in msg  or "在吗" in msg or "在嘛" in msg or "在？" in msg

def isFirstNeed(msg):
	return ("是" in msg or "需要" in msg) and ("不" not in msg)

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

def studyProgress(remark_name):
	file = os.path.join(os.getcwd()+os.path.sep+user_path+os.path.sep+remark_name+".conf")
	if not os.path.exists(file):
		return 1
	else:
		conf = configparser.ConfigParser()
		conf.read(file)
		last_file = int(conf.get(store_section, store_last_file))
		time = conf.get(store_section, store_last_time)
		last_time = datetime.datetime.strptime(time, date_format)
		interval = datetime.datetime.now() - last_time
		if last_file >= max_file:
			return max_file
		elif interval.seconds > date_interval:
			return last_file + 1
		else:
			return last_file

def recordPrgress(remark_name, nick_name, cur_file):
	file = os.path.join(os.getcwd()+os.path.sep+user_path+os.path.sep+remark_name+".conf")
	conf = configparser.ConfigParser()
	if os.path.exists(file) :
		conf.read(file)
		last_file = int(conf.get(store_section, store_last_file))
		if last_file < cur_file :
			conf.set(store_section, store_last_file, str(cur_file))
			conf.set(store_section, store_last_time, datetime.datetime.now().strftime(date_format))
	else:
		conf.add_section(store_section)
		conf.set(store_section, store_name, remark_name)
		conf.set(store_section, store_nick_name, nick_name)
		conf.set(store_section, store_last_file, str(cur_file))
		conf.set(store_section, store_last_time, datetime.datetime.now().strftime(date_format))
	conf.write(open(file,"w"))

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

try:
	log_to_mail("system start now")
	sched = BackgroundScheduler()
	@sched.scheduled_job('interval', id="qrcode_check", seconds=60)
	def qrcode_check():
		global md5
		if os.path.exists(qrcode_file):
			temp_md5 = md5sum(qrcode_file)
			if temp_md5 != md5:
				log_to_mail("Dengdeng need login, please scan qr code", qrcode_file)
				md5 = temp_md5

	sched.start()
	bot = Bot(cache_path=True,console_qr=False)
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

	have_asked = {}
	# 回复 my_friend 的消息 (优先匹配后注册的函数!)
	#@bot.register(my_friend)
	@bot.register(Friend, TEXT)
	def reply_my_friend(msg):
		msg_text = msg.text.strip()
		user = msg.sender.remark_name
		logging.warning("ready to reply to friend " + user)
		if user not in have_asked:
			have_asked[user] = False
		#如果提问过
		if have_asked[user]:
			have_asked[user] = False
			#回复第一章(只有第一章的回复为是,否)
			if isFirstNeed(msg_text):
				recordPrgress(user,msg.sender.nick_name, 1)
				msg.sender.send_file(get_article(1))
				logging.warning("replied the first article to " + user)
				return
			#回复后续章
			next_number = isNextNumber(msg_text)
			if next_number !=0 :
				progress = studyProgress(user)
				if (progress >= next_number):
					recordPrgress(user, msg.sender.nick_name, next_number)
					msg.sender.send_file(get_article(next_number))
					logging.warning("replied " + str(next_number) + " article to " + user)
					return
				else:
					logging.warning("will reply no pemission for " + str(next_number) + " article to " + user)
					return reply_no_permission.format(progress)
			logging.warning("will reply no need to " + user)
			return reply_no_need

		else:
			logging.warning("will reply question to " + user)
			have_asked[user] = True
			progress = studyProgress(user)
			if 1 == progress:
				return reply_ask_first.format(msg.sender.nick_name)
			else:
				return reply_ask_next.format(msg.sender.nick_name, progress-1, progress)


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

	@sched.scheduled_job('interval', seconds=20)
	def heart_beat_alive():
		logging.warning("alive:" + str(bot.alive))
		if not bot.alive:
			logging.warning("not alive, send email")
			log_to_mail("dengdeng not alive now")
			sys.exit();
		else:
			logging.warning("alive, continue")

	bot.join()

except ResponseError as r:
	logging.warning("encounter ResponseError")
	log_to_mail("dengdeng encounter ResponseError")
	sys.exit();
except Exception as e:
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
