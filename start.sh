if [ -f .env ]
then
	python main.py
else
	echo DISCORD_TOKEN=$DISCORD_TOKEN >> .env

	echo DB_PATH=$DB_PATH >> .env
	echo DB_NAME=$DB_NAME >> .env

	echo CHANNEL_YT=$CHANNEL_YT >> .env
	echo CHANNEL_SP=$CHANNEL_SP >> .env
	
	echo DISCORD_GUILD=$DISCORD_GUILD >> .env

	mkdir $DB_PATH
	
	python main.py
fi 
