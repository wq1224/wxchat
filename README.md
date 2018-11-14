# wxchat
pip3 install -U wxpy
pip3 install pycnnum
pip3 install apscheduler 

docker run -d -it  \
-e "QRCODE_FILE=/usr/src/app/wxchat/log/QR.png" \
-e "QRCODE_URL=http://106.14.0.107/scriptures/QR.png" \
-e "API_URL=http://106.14.0.107:80/angular/" \
-v log:/usr/src/app/wxchat/log \
9237d3c40489

docker run -d -it  \
-e "QRCODE_FILE=/usr/src/app/wxchat/log/QR.png" \
-e "QRCODE_URL=http://111.231.144.146:8080/qr/QR.png" \
-e "API_URL=http://111.231.144.146:8080/appWeb/" \
-v /usr/java/tomcat/apache-tomcat-8.5.16/webapps/qr:/usr/src/app/wxchat/log \
docker.io/wq1224/wxchat:V1


docker run -d -it  \
-e "QRCODE_FILE=/usr/src/app/wxchat/log/QR.png" \
-e "QRCODE_URL=http://106.14.0.107/scriptures/QR.png" \
-e "API_URL=http://106.14.0.107:80/angular/" \
-v log:/usr/src/app/wxchat/log \
--entrypoint bash \
afebeda3436f318f3e6c3786b3fa0a6220ec125b170aae719ade18d586f6ceed 


docker run -d -it  \
-e "QRCODE_FILE=/usr/src/app/wxchat/log/QR.png" \
-e "QRCODE_URL=http://106.14.0.107/scriptures/QR.png" \
-e "API_URL=http://106.14.0.107:80/angular/" \
-v log:/usr/src/app/wxchat/log \
--entrypoint ./docker-entrypoint.sh \
9237d3c40489

docker build .
docker tag local-image:tagname new-repo:tagname
docker push new-repo:tagname
docker exec -it containerid /bin/bash
