import os 

DISCORD_TOKEN = str(os.environ["DISCORD_TOKEN"])
DISCORD_GUILD = str(os.environ["DISCORD_GUILD"])

DB_PATH = str(os.environ["DB_PATH"])
DB_NAME = str(os.environ["DB_NAME"])

CHANNEL_YT = str(os.environ["CHANNEL_YT"])
CHANNEL_SP = str(os.environ["CHANNEL_SP"])

DB_JOIN = str(os.environ["DB_PATH"]) + "/" + str(os.environ["DB_NAME"])

already_start = False

print(f"env var =================== discord token --> {DISCORD_TOKEN} \ndiscord guild --> {DISCORD_GUILD} \ndb name --> {DB_NAME} \ndb path --> {DB_PATH} \nvideo channel id --> {CHANNEL_YT} \nmusic channel id --> {CHANNEL_SP} \n--> {DB_JOIN}")

for folder in os.listdir(path="."):
    if str(folder) == DB_NAME:
        already_start = True

if already_start == True:
    os.system("python main.py")

else:
    with open(".env", "w") as env:
        env.write("DISCORD_TOKEN=" + DISCORD_TOKEN + "\n")
        env.write("DISCORD_GUILD=" + DISCORD_GUILD + "\n")

        env.write("DB_PATH=" + DB_PATH + "\n")
        env.write("DB_NAME=" + DB_NAME + "\n")

        env.write("CHANNEL_YT=" + CHANNEL_YT + "\n")
        env.write("CHANNEL_SP=" + CHANNEL_SP + "\n")

    with open(".env", "r") as env:
        print("\n.env file ===================\n", env.read())
    
    os.system(f"mkdir {DB_PATH}")
    os.system("ls -larth && pwd")
    os.system(f"touch {DB_JOIN} && ls -larth && ls -larth {DB_PATH}")

    os.system("python main.py")