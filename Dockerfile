FROM python:3.9.1-buster
MAINTAINER DarkOnion0

WORKDIR /usr/src/ADZTBot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py start.sh ./

RUN mkdir lib
COPY lib/* ./lib/
RUN chmod +x start.sh

ENV DISCORD_TOKEN=null
ENV DB_PATH=data
ENV DB_NAME=bot_data
ENV CHANNEL_YT=null
ENV CHANNEL_SP=null

CMD ["sh", "start.sh"]