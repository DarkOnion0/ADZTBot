import os
import random
import discord
import requests
import time
from bs4 import BeautifulSoup
from discord.ext import commands
from dotenv import load_dotenv
from lib import db
from link_preview import link_preview

# START

print("BOT STARTED !!!")

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DB_PATH = os.getenv("DB_PATH") + "/" + os.getenv("DB_NAME")
CHANNEL_YT = int(os.getenv("CHANNEL_YT"))
CHANNEL_SP = int(os.getenv("CHANNEL_SP"))
GUILD = os.getenv('DISCORD_GUILD')
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX")

client = discord.Client()
bot = commands.Bot(command_prefix=COMMAND_PREFIX)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

print("\n .ENV file data :", TOKEN, DB_PATH, CHANNEL_SP, CHANNEL_YT, COMMAND_PREFIX)

print(DB_PATH)

DataUser = db.user(DB_PATH)
DataPost = db.vote(DB_PATH)
v = "v4.0.2"


client = discord.Client()
bot.remove_command("help")
# COMMAND
# help
@bot.command(name="help")
async def help(ctx):
    start_time = time.time()
    
    urlDict = link_preview.generate_dict("https://github.com/DarkOnion0/ADZTBot")
    embed = discord.Embed(
        title=urlDict["title"],
        description="Check the command section on the README\n\n"
        + urlDict["description"],
        url="https://github.com/DarkOnion0/ADZTBot#command-list",
        colour=discord.Color.gold(),
    )

    embed.set_author(
        name="HELP",
        icon_url="https://raw.githubusercontent.com/DarkOnion0/ADZTBot/master/logo.png",
        url="https://github.com/DarkOnion0/ADZTBot",
    )
    embed.set_thumbnail(url=urlDict["image"])
    
    end_time = "%s seconds" % (time.time() - start_time)
   
    embed.set_footer(text=v+ " | " + end_time)

    await ctx.send(embed=embed)


# linux


@bot.command(name="linux", help="Linux Propagande", pass_context=True)
async def linux(ctx, *arg):
    arg = list(arg)
    print(len(arg), type(arg), arg)

    # info command, give a list of linux distro
    if arg[0] == "info":
        if len(arg) == 1:
            #emebed = discord.Embed(color=discord.Color.orange())
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
@bot.command(name="pouf", help="simulate a coins launch (pile ou face game)")
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
    authorId = int(ctx.message.author.id)
    author = str(ctx.message.author)
    author = author.split("#")

    user = await bot.fetch_user(authorId)
    print(user)

    # print(arg) # debug
    if arg[0] == "init":
        # print(ctx.message.author, "Hello") # debug

        result = DataUser.add(author[0], authorId)

        result = int(result)
        if result == 0:
            await ctx.send("**:warning: ERROR :** You already exist in the database")
        elif result == 1:
            await ctx.send(
                "Welcome {},\nYour profile has been setup successfully :+1:".format(
                    author[0]
                )
            )
    if arg[0] == "update":
        DataUser.update(author[0], authorId, arg=("update_name", arg[1]))

        await ctx.send(
            "**:star: SUCCSES :** Your {} has been succsesfully updated".format(arg[1])
        )

# user stats
@bot.command(name="ustats")
async def ustasts(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    roles = [role for role in member.roles]

    print(member.id)

    result = DataUser.stats(member.id)
    try:
        result = list(result)
    except TypeError:
        result = [0.1]

    print(result)

    embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

    embed.set_author(name=f"User Stats | {member.display_name}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Summon by {ctx.author}", icon_url= ctx.author.avatar_url)

    embed.add_field(name="Name", value=member.mention, inline=False)
    embed.add_field(name="ID", value=member.id, inline=False)

    if result[0] == 1:
        embed.add_field(name="Description", value=str(result[7]))
        embed.add_field(name="Games", value=str(result[8]), inline=False)
        embed.add_field(name=f"Level ({result[2]})", value=f"**:trophy: experience |** {result[9]}", inline=False)
        embed.add_field(name=f"Post ({result[3]})", value=result[4], inline=False)
    
    embed.add_field(name="Created at", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
    embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]), inline=False)



    embed.add_field(name="Bot ?", value=member.bot)

    await ctx.send(embed=embed)


# post command
@bot.command(name="post", pass_context=True, add_reactions=True, embed_links=True)
async def post(ctx, *arg):
    arg = list(arg)
    author = str(ctx.message.author)
    authorId = int(ctx.message.author.id)

    print(authorId)

    author = author.split("#")

    result = DataPost.post(authorId, arg[0], arg[1])
    print(result, type(result))
    muId, answer = result

    print(answer)
    try:
        url = arg[1]
        urlDict = link_preview.generate_dict(url)
        # making requests instance 
        reqs = requests.get(url) 
        # using the BeaitifulSoup module 
        soup = BeautifulSoup(reqs.text, 'html.parser') 
        # displaying the title 
        for title in soup.find_all('title'): 
          title = title.get_text()
        download_passed = True
    except:
        download_passed = False

    if download_passed == True:
        if answer == 0.1:  # ERROR -> profile doesn't exist
            await ctx.send(
                "**:warning: ERROR 1 :** please create a profile by typing `/profile init`"
            )
        if answer == 0.2:  # ERROR -> already post
            await ctx.send(
                "**:warning: ERROR 2 :** please don't post a link that was already post"
            )
        if answer == 1:  # SUCCESS
            print("Hello")

            #url = arg[1]
            #urlDict = link_preview.generate_dict(url)


            if arg[0] == "m":
                msg = "[{}]({})".format(urlDict["description"], arg[1])
                embed = discord.Embed(colour=discord.Color.green())
                channelM = bot.get_channel(int(CHANNEL_SP))
                print(channelM, int(CHANNEL_SP))
            if arg[0] == "v":
                msg = "[{}]({})".format(urlDict["title"], arg[1])
                embed = discord.Embed(colour=discord.Color.red())
                channelM = bot.get_channel(int(CHANNEL_YT))
            embed.set_author(
                name="Posted by {}".format(author[0]), icon_url=ctx.author.avatar_url
            )

            if arg[0] == "m":
                embed.add_field(name="Music #{}".format(muId), value=msg, inline=True)
            if arg[0] == "v":
                embed.add_field(name="Video #{}".format(muId), value=msg, inline=True)

            embed.set_image(url=urlDict["image"])

            await channelM.send(
                embed=embed
            )  # send message in the channel for music proposal
            await ctx.send(
                "**:star: SUCCESS : **Your post has been registred successfully \n```type = {} \nlink = {} \nid = {}```".format(
                    arg[0], arg[1], muId
                )  # send message in the current channel
            )
    else:
        await ctx.send("**:warning: ERROR 3:** Please post a valid url")


# vote command


@bot.command(name="vote", pass_context=True)
async def vote(ctx, *arg):

    arg = list(arg)
    author = str(ctx.message.author)
    author = author.split("#")
    authorId = int(ctx.message.author.id)

    print(author, arg)

    if len(arg) != 3:
        msg = "**:warning: ERROR :warning:** please specify *v or m* option, after the music id and finally the vote (+ or -)"
        await ctx.send(msg)
        
    if arg[2] == "+" or arg[2] == "-":
        result = DataPost.vote(authorId, arg[0], arg[1], arg[2])
    else:
        result = None
        await ctx.send("**:warning: ERROR 0 :** please put `+` or `-` for voting")

    if result == 0.1:
        await ctx.send(
            "**:warning: ERROR 1 :** please create a profile by typing `/profile init`"
        )
    if result == 0.2:
        await ctx.send(
            "**:warning: ERROR 2 :** the post id `{}` doesn't exist in the `{}` categorie".format(
                arg[1], arg[0]
            )
        )
    if result == 0.3:
        await ctx.send("**:warning: ERROR 3 :** please don't revote on the same post")
    if result == 1:
        await ctx.send(
            "**:star: SUCCESS :** Your vote has been successfully registred {}".format(
                author[0]
            )
        )


# stat command


@bot.command(name="pstats", pass_context=True)
async def pstats(ctx, *arg):

    arg = list(arg)
    author = str(ctx.message.author)
    author_id = int(ctx.message.author.id)
    author = author.split("#")

    if len(arg) != 2:
        await ctx.send(
            "**:warning: ERROR :** please specify the categorie and the id or the username"
        )

    else:
        result = DataPost.stats(arg[0], arg[1])
        result, type_f, postid_f, user_f, link_f, score_f, vote_user_f = result

        if result == 0.1:
            await ctx.send("**:warning: ERROR 1 :** the post doesn't exist")
        elif result == 1:
            user_f_id = await bot.fetch_user(user_f)
            user_f_name = str(user_f_id).split("#")

            url = link_f
            urlDict = link_preview.generate_dict(url)

            msg = "[{}]({})".format(urlDict["description"], link_f)

            r = random.randint(0, 255)  # random color chooser
            g = random.randint(0, 255)
            b = random.randint(0, 255)

            if type_f == "m":
                type_f = "Music"
            elif type_f == "v":
                type_f = "Video"

            embed = discord.Embed(colour=discord.Color.from_rgb(r, g, b))

            embed.set_author(name="{}".format(type_f))

            embed.add_field(name="Title", value=msg, inline=False)
            embed.add_field(name="User", value=user_f_name[0], inline=True)
            embed.add_field(name="Id", value=postid_f, inline=True)
            embed.add_field(name="Score", value=score_f, inline=True)

            embed.set_thumbnail(url=urlDict["image"])

            print(ctx.author.avatar_url)

            await ctx.send(embed=embed)


bot.run(TOKEN)
