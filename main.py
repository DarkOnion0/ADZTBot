import os
import random
import discord

from discord.ext import commands
from dotenv import load_dotenv

# START

print("BOT STARTED !!!")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

client = discord.Client()
# COMMAND

## linux
@bot.command(name='linux', help='Linux Propagande')
async def linux(ctx):

    msg='Linux > ALL **| YOU MUST CHECK** https://archlinux.org/'

    response = msg
    await ctx.send(response)

## dice
@bot.command(name='dice', help='Simulates rolling dice between 0 and 10')
async def roll(ctx):
    nb = random.randint(0,10)
    response = ":game_die: | {}".format(nb)

    await ctx.send(response)

## pile ou face 
@bot.command(name='pouf', help='Pile ou Face game, are you lucky ? Bet and try it :)')
async def pouf(ctx):
    nb = random.randint(1,2)

    if nb == 1:
        await ctx.send(':full_moon_with_face: | pile')
    else:
        await ctx.send(':new_moon_with_face: | face')

## user info
@bot.command(name='profile', help='Main command for setup a Server Profile (en dev)')
async def profile(ctx):
    msg = "**TU COMPRENDS PAS LA PHRASE: EN DEV**"

    await ctx.send(msg)

bot.run(TOKEN)

