while true; do
	echo "kill python process"
	pkill -f /Users/i314017/study/wxchat/test.py
	echo "start python3"
	nohup /usr/local/bin/python3 /Users/i314017/study/wxchat/test.py &
	echo "end"
	sleep 3600
done
