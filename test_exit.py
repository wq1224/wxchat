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
		logging.warning("reply start")
		my_friend.send("测试回复")
		#my_friend.send_file(file)

	# my_friend.send(result)
	#bot.logout()
	sched = BackgroundScheduler()

	@sched.scheduled_job('interval', minutes=15)
	def send_msg():
		logging.warning("scheduler job start")
		my_friend.send("测试")
		#my_friend.send_file(file)

	@sched.scheduled_job('interval', seconds=20)
	def heart_beat():
		logging.warning("alive:" + str(bot.alive))
		if not bot.alive:
			logging.warning("not alive, send email")
			s.send_message(msg)	
			sys.exit();
		else:
			logging.warning("alive, continue")
	
	sched.start()
	bot.join()
	#embed();
	# while True:
	# 	time.sleep(2)    #其他任务是独立的线程执行
	# 	print('sleep!')
except Exception as e:
	logging.warning("encounter ResponseError, will retry... ", e)
	s.send_message(msg)
	sys.exit();
