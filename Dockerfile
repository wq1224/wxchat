FROM python:3

WORKDIR /usr/src/app/wxchat

COPY requirements.txt ./
COPY test.py ./
COPY /budda ./budda
RUN pip install --no-cache-dir -r requirements.txt

RUN  cd `python -m site | grep -oP -m1  "(?<=').*site-packages(?=')"`

# RUN git clone https://github.com/wq1224/wxchat.git
# COPY . .

# CMD [ "python", "./your-daemon-or-script.py" ]