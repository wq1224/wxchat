# wxchat
pip3 install -U wxpy
pip3 install pycnnum
pip3 install apscheduler 


docker run -d -it  \
-e "QRCODE_FILE=/usr/src/app/wxchat/log/QR.png" \
-e "QRCODE_URL=http://106.14.0.107/scriptures/QR.png" \
-e "API_URL=http://106.14.0.107:80/angular/" \
-v log:/usr/src/app/wxchat/log \
--entrypoint bash \
2c8c309336e6 


docker run -d -it  \
-e "QRCODE_FILE=/usr/src/app/wxchat/log/QR.png" \
-e "QRCODE_URL=http://106.14.0.107/scriptures/QR.png" \
-e "API_URL=http://106.14.0.107:80/angular/" \
-v log:/usr/src/app/wxchat/log \
2c8c309336e6

docker run -d -it  \
-e "QRCODE_FILE=/usr/src/app/wxchat/log/QR.png QRCODE_URL=http://106.14.0.107/scriptures/QR.png API_URL=http://106.14.0.107:80/angular/" \
-v log:/usr/src/app/wxchat/log \
c7e557e692b5 