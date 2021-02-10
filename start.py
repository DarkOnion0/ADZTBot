import os 

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
DISCORD_GUILD = os.environ["DISCORD_GUILD"]

DB_PATH = os.environ["DB_PATH"]
DB_NAME = os.environ["DB_NAME"]

CHANNEL_YT = os.environ["CHANNEL_YT"]
CHANNEL_SP = os.environ["CHANNEL_SP"]

already_start = False

print(f"discord token --> {DISCORD_TOKEN} \ndiscord guild --> {DISCORD_GUILD} \ndb name --> {DB_NAME} \ndb paht --> {DB_PATH} \nvideo channel id --> {CHANNEL_YT} \nmusic channel id {CHANNEL_SP}")

for folder in os.listdir(path="."):
    if str(folder) == DB_NAME:
        already_start = True

if already_start == True:
    os.system("python main.py")

else: