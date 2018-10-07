FROM python:3

WORKDIR /usr/src/app/wxchat

ENV QRCODE_FILE /usr/src/app/wxchat/log/QR.png

COPY requirements.txt ./
COPY test.py ./
COPY docker-entrypoint.sh ./
COPY /budda ./budda
RUN  pip install --no-cache-dir -r requirements.txt \
	 && chmod +x docker-entrypoint.sh \
     && cd `python -m site | grep -oP -m1  "(?<=').*site-packages(?=')"`/urllib3 \
	 && mv fields.py fields.py.bak \
	 && wget https://gist.githubusercontent.com/littlecodersh/e93532d5e7ddf0ec56c336499165c4dc/raw/9ef4f11c7dca8f3e0c8fa4b32482cbe20e458668/fields.py \
	 && cd `python -m site | grep -oP -m1  "(?<=').*site-packages(?=')"`/itchat \
	 && sed -i 's/utils.print_qr/#&/' components/login.py \ 
	 && apt-get update \
	 && apt-get install -y vim \
	 && apt-get install -y supervisor \
	 && cat /etc/supervisor/supervisord.conf >> /supervisord.conf \
	 && echo "[program:wxchat]" >> /supervisord.conf \
     && echo "command=python3 test.py     ; the program (relative uses PATH, can take args)" >> /supervisord.conf \
     && echo "directory=/usr/src/app/wxchat    		; directory to cwd to before exec (def no cwd)" >> /supervisord.conf \
     && echo "umask=022                     ; umask for process (default None)" >> /supervisord.conf \
     && echo "autorestart=true              ; when to restart if exited after running (def: unexpected)" >> /supervisord.conf \
     && echo "stopsignal=QUIT               ; signal used to kill process (default TERM)" >> /supervisord.conf \
     && echo "user=0                     ; setuid to this UNIX account to run the program" >> /supervisord.conf \
     && echo "redirect_stderr=true          ; redirect proc stderr to stdout (default false)" >> /supervisord.conf \
     && echo "stdout_logfile=/usr/src/app/wxchat/log/wxchat.log        ; stdout log path, NONE for none; default AUTO" >> /supervisord.conf

# ENTRYPOINT ["./docker-entrypoint.sh"]
# RUN git clone https://github.com/wq1224/wxchat.git
# COPY . .
# supervisord -c supervisord.conf
# CMD [ "supervisord", "-c", "supervisord.conf" ]
# CMD [ "supervisord", "-c", "/supervisord.conf" ]
CMD supervisord -c /supervisord.conf && tail -f /dev/null