# ADZTBot
A little discord bot make just for fun :grin: with Discord.py framework and shared with docker

# Features :rocket: 
* vote command for youtube and spotify post
* linux command (dispaly information about linux)
* a simple profile systeme (beta)

# TO-DO 💡
* create game invite (a message that ping everyone who accept to be notify to play a game with the people)
* integreate webhooks

# Installation
## Docker 🐋
1. clone the repository or download the release
2. build the docker image, `docker build -t --no-cache adztbot .`
3. start the container with a `.env` file for the environement variables, `docker run --env-file=.env adztbot:latest`

## Linux 🐧
1. clone the repository or download a release
2. install the requiered librairies, `pip install -r requirements.txt`
3. create the data folder, `mkdir data`
4. create a .env file in the script directory
5. start the bot, `python main.py` 

## ENV variable / file
```env
# MANDATORY variable (it will contain the discord bot token for the python script)
DISCORD_TOKEN= your_discord_bot_token

# Using docker you can omit this line in your .env file (defaut value = data), with a direct script you MUST specify the name (don't putt the '/' at the end)
DB_PATH= your_db_path

# Using docker you can omit this line in your .env file (defaut value = bot_data), with a directe script you MUST specify the name
DB_NAME= your_db_name
```
