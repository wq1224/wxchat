import os
import requests
import datetime
import pdb
import re
import time
import hashlib
import base64
import json

base_url = "https://api.xfyun.cn"

sentence = "今天星期几"
sentence_base64 = str(base64.b64encode(sentence.encode("utf-8")),'utf-8')
#sentence_base64 = "5LuK5aSp5pif5pyf5Yeg"
payload_text = "text={0}".format(sentence_base64)
payload = {"text": sentence_base64 }

appid = "5a27a80b"
app_key = "59f27e4c48e04dfdbb8fcef29c8ec157"
cur_time = int(time.time())
param = "eyJzY2VuZSI6Im1haW4iLCAidXNlcmlkIjoidXNlcl8wMDAxIn0="
checkSum = app_key + str(cur_time) + param + payload_text

header = {
	"X-Appid": appid,
	"X-CurTime": str(cur_time),
	"X-Param": param,
	"X-CheckSum": hashlib.md5(checkSum.encode('utf-8')).hexdigest()
}

url = base_url + "/v1/aiui/v1/text_semantic"

r = requests.post(url, data=payload, headers=header)

print (r.json())
print (json.dumps(r.json(),indent=4))