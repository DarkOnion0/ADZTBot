if [ -f .env ]
then
	python main.py
else
	echo DISCORD_TOKEN=$DISCORD_TOKEN >> .env
	echo DB_PATH=$DB_PATH >> .env

	mkdir $DB_PATH
	
	python main.py
fi 
