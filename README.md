# ADZTBot

![Docker](https://github.com/DarkOnion0/ADZTBot/workflows/Docker/badge.svg?branch=master)

A little discord bot make just for fun :grin: with Discord.py framework and shared with docker. The project is currently in **BETA**, so it can have some bugs

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

1. pull the image from the github registry `docker pull ghcr.io/darkonion0/adztbot:<release>` or `docker pull ghcr.io/darkonion0/adztbot:latest` for the unstable one
2. start the container with a `.env` file for the environement variables, `docker run -dv your_path_for_data:/usr/src/ADZTBot/the_name_of_the_data_folder_choosen --env-file=.env --name ADZTBot ghcr.io/darkonion0/adztbot:<choosen_version>`

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

- `/profile [COMMAND] [ARG]`
	- **[COMMAND]**
		- `init` an argument that create your profile in the database
		- `update` an argument that update your `user_id` or your `username`
    		- **[ARG]** `id` let the user update his id if he doesn't exist (only for the [v2.1.0](https://github.com/DarkOnion0/ADZTBot/releases/tag/v2.2.0) breaking changes)
			- **[ARG]** `name` let the user update his username, making the admin jobs easier :grin:
- `/ustats [USER]`
  - **[USER]** you can put a username for getting the user's information and stats or anything else for getting yours

- `/post [CATEGORIE] [LINK]` let user post music or video
	- **[CATEGORIE]** it can be `m` (music) or `v` (vidéo) option
	- **[LINK]** it is the link you want to share

- `/vote [CATEGORIE] [ID] [VOTE]` let user vote on existing post
	- **[CATEGORIE]** it can be `m` (music) or `v` (vidéo) option
	- **[ID]** it's the id given after the `#` in the message
	- **[VOTE]** it can be `+` or `-` (you can only vote onetime by post, **⚠️ a vote is definitive**)
	
- `/pstats [CATEGORIE] [ID]` let the user knows the stat on a post
	- **[CATEGORIE]** it can be `m` (music) or `v` (vidéo) option
	- **[ID]** it's the id given after the `#` in the message

# Contributing
- We need your help :handshake:
