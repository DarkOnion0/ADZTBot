# ADZTBot

A little discord bot make just for fun :grin: with Discord.py framework and shared with docker

# Features :rocket:

- vote command for youtube and spotify post (beta)
- linux command (dispaly information about linux)
- lot of other funny command, see [command list](#command-list)

# TO-DO 💡

- create game invite (a message that ping everyone who accept to be notify to play a game with the people)
- integreate webhooks
- a simple profile systeme (in work)
- basic administration

# Installation

## Docker 🐋

1. clone the repository or download the release
2. build the docker image, `docker build -t --no-cache adztbot .`
3. start the container with a `.env` file for the environement variables, `docker run -dv your_path_for_data:/usr/src/ADZTBot/the_name_of_the_data_folder_choosen --env-file=.env adztbot:latest`

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

CHANNEL_YT= your_channel_for_video_id
CHANNEL_SP= your_channel_for_music_id
```

# Command list

- `/pouf` simulate a coins launch (pile ou face game)

- `/dice` simulate a dice

- `/linux info [ARG]` give info on linux and linux distribution
	- **[ARG]** can be a anything or the name of a linux distribution list in the base command

- `/profile [ARG]`
	- **[ARG]** right now the only things you can pass to the command is the `init` option
		- `init` an argument that create your profile in the database

- `/post [CATEGORIE] [LINK]` let user post music or video
	- **[CATEGORIE]** it can be `m` (music) or `v` (vidéo) option
	- **[LINK]** it is the link you want to share

- `/vote [CATEGORIE] [ID] [VOTE]` let user vote on existing post
	- **[CATEGORIE]** it can be `m` (music) or `v` (vidéo) option
	- **[ID]** it's the id given after the `#` in the message
	- **[VOTE]** it can be `+1` or `-1` (you can only vote ontime by post, **⚠️ a vote is definitive**)

# Contributing
- We need your help :handshake:
