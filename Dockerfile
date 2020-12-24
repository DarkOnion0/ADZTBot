FROM python:3.9.1-buster
MAINTAINER DarkOnion0

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py start.sh ./

RUN mkdir lib
COPY lib/* ./lib/
RUN chmod +x start.sh

ENV DISCORD_TOKEN=null
ENV DB_PATH=data
ENV DB_NAME=bot_data

CMD ["sh", "start.sh"]
