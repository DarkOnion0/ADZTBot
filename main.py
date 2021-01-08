import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from lib import db

# START

print("BOT STARTED !!!")

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DB_PATH = os.getenv("DB_PATH") + "/" + os.getenv("DB_NAME")
print(DB_PATH)

DataUser = db.user(DB_PATH)
DataPost = db.vote(DB_PATH)

bot = commands.Bot(command_prefix="/")

client = discord.Client()
# COMMAND

# linux


@bot.command(name="linux", help="Linux Propagande", pass_context=True)
async def linux(ctx, *arg):
    arg = list(arg)
    print(len(arg), type(arg), arg)

    # info command, give a list of linux distro
    if arg[0] == "info":
        if len(arg) == 1:
            msg = "**Linux > ALL | YOU MUST CHECK ONE OF THESE LINUX DISTRO :** \n***Arch based distro:*** \n- archlinux \n- manjaro \n- endeavourOS \n\n***RPM distro*** \n- fedora \n- centos stream \n\n***Debian / Ubuntu based distro*** \n- debian \n- linux mint \n- PopOS \n- ubuntu flavour \n\nhttps://tenor.com/view/mst3k-join-us-come-gif-13947932"
            await ctx.send(msg)
        if len(arg) == 2:
            if arg[1] == "archlinux":
                msg = "**ArchLinux**\n***- WebSite |*** https://archlinux.org/ \n***- Wikipedia |*** https://en.wikipedia.org/wiki/Arch_Linux \n***- Level |*** Hard (it is not a distro for people who don't know or want to understand linux)\n***- Comment |*** I think it's one or the best linux distribution in the world :earth_africa:"
                await ctx.send(msg)


# dice
@bot.command(name="dice", help="Simulates rolling dice between 0 and 10")
async def roll(ctx):
    nb = random.randint(0, 10)
    response = ":game_die: | {}".format(nb)

    await ctx.send(response)


# pile ou face


@bot.command(name="pouf", help="Pile ou Face game, are you lucky ? Bet and try it :)")
async def pouf(ctx):
    nb = random.randint(1, 2)

    if nb == 1:
        await ctx.send(":full_moon_with_face: | pile")
    else:
        await ctx.send(":new_moon_with_face: | face")


# user info


@bot.command(
    name="profile",
    help="Main command for setup a Server Profile (en dev)",
    pass_context=True,
)
async def profile(ctx, *arg):
    # arg = str(arg)
    # arg = arg.split(" ")

    # print(arg) # debug
    if arg[0] == "init":
        # DataUser.add(ctx.message)
        # print(ctx.message.author, "Hello") # debug
        author = str(ctx.message.author)
        author = author.split("#")
        DataUser.add(author[0])
        await ctx.send(
            "Welcome {},\nYour profile has been setup successfully :+1:".format(
                author[0]
            )
        )
    else:
        msg = "**ERROR**\n veuillez mettre un des arguments suivant :\n`init | init your profile in the database`"
        await ctx.send(msg)


# post command


@bot.command(name="post", pass_context=True)
async def post(ctx, *arg):
    arg = list(arg)
    author = str(ctx.message.author)
    author = author.split("#")

    if arg[0] == "m": # music option
        answer = str(DataPost.post(author[0], "m", arg[1]))
        if answer == "0.1": # ERROR -> profile doesn't exist
            await ctx.send(
                "**:warning: ERROR 1 :** please create a profile by typing `/profile init`"
            )
        if answer == "0.2": # ERROR -> already post
            await ctx.send(
                "**:warning: ERROR 2 :** please don't post a link that was already post"
            )
        if answer == "1": # SUCCESS
            await ctx.send(
                "**:star: SUCCESS : **Your post has been registred successfully"
            )
    elif arg[0] == "v": # video option
        print("vidéo otpion")
    else:
        msg = "**:warning: ERROR :warning:** please specify *v or m* option"
        await ctx.send(msg)


# vote command


@bot.command(name="vote", pass_context=True)
async def vote(ctx, *arg):
    arg = list(arg)
    if arg[0] == "m":
        print("music option")
    elif arg[0] == "v":
        print("vidéo otpion")
    else:
        msg = "**:warning: ERROR :warning:** please specify *v or m* option"
        await ctx.send(msg)


bot.run(TOKEN)
