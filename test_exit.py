from wxpy import *
import time
import sys
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
import os
from email.message import EmailMessage
import logging
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
mail = "337569887@qq.com"
passwd = "ddtgzhtuejxpbjig"
#file = "/Users/i3/study/wxchat/budda/第十七讲 什么是因果不虚(backup).pdf"
try:
	print("scheduler job start")
	#raise Exception("error")
	msg = EmailMessage()
	msg.set_content("email test")
	msg['Subject'] = 'bot fail'
	msg['From'] = mail
	msg['To'] = mail
	s = smtplib.SMTP_SSL("smtp.qq.com",465)
	s.login(mail, passwd)
	#s.send_message(msg)
	#pdb.set_trace()
	bot = Bot(cache_path=False,console_qr=True)
	# filepath = os.path.join(os.getcwd()+os.path.sep+path+os.path.sep+file[0:file.rindex(".")])
	# bot.file_helper.send_file(filepath+".pdf")
	# bot.file_helper.send_file(filepath+".docx")
	#my_friend = bot.friends().search('灯灯')[0]
	my_friend2 = bot.friends().search('灯灯')[0]
	my_friend = bot.file_helper


	@bot.register(my_friend2, TEXT)
	def reply_my_friend(msg):
		print("reply start, pid: " + str(os.getpid()))
		my_friend.send("测试回复")
		#my_friend.send_file(file)

	# my_friend.send(result)
	#bot.logout()
	sched = BackgroundScheduler()

	@sched.scheduled_job('interval', minutes=15)
	def send_msg():
		print("scheduler job start, pid:  "  + str(os.getpid()))
		my_friend.send("测试")
		#my_friend.send_file(file)

	@sched.scheduled_job('interval', seconds=20)
	def heart_beat():
		print("alive:" + str(bot.alive))
		if not bot.alive:
			s.send_message(msg)	
			sys.exit();
	
	sched.start()
	bot.join()
	#embed();
	# while True:
	# 	time.sleep(2)    #其他任务是独立的线程执行
	# 	print('sleep!')
except ValueError as v:
	print("encounter ResponseError, will retry... ", e)
except Exception as e:
	print("encounter ResponseError, will retry... ", e)
	sys.exit();
