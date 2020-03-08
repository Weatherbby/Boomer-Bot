import discord
from discord.ext import commands, tasks
from itertools import cycle
import youtube_dl
import asyncio
import time
import datetime

log = open("log.txt", "w")
song = 'https://www.youtube.com/watch?v=Z_c95XKwUvI'
source = "C:\\Users\\alexa\\Desktop\\Programming\\DiscordBot\\boomer.mp3"
TOKEN = 'Njg1OTE4NDkzMzgzNTg5OTUx.XmPpdQ.hTAuhNg_-08_0SbsL4WX4CICVNs'
bot = commands.Bot(command_prefix = '.')

boomers = []
players = {}

statuses = cycle(['DeStRoYiNg BoOmErS', 'dEsTrOyInG bOoMeRs'])

@bot.event
async def on_ready():
    change_status.start()
    await bot.change_presence(status = discord.Status.idle, activity= discord.Game('DeStRoYiNg BoOmErS'))
    print('BOOMER DESTROYER online')


@bot.command()
async def boomer(ctx, member : discord.Member, times = 1):
    await ctx.message.channel.purge(limit = 1)
    if "boomer" in [role.name.lower() for role in member.roles]:
        for i in range(times):
            await ctx.send(f'BOOMER {member.mention}')
    else:
        await ctx.send(f'User {member.name} is not a boomer.')

@bot.command()
async def clear(ctx, msgs:int):
    await ctx.message.channel.purge(limit = msgs)

@bot.command()
async def longplay(ctx, member : discord.Member):
    channel = member.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio(source), after=lambda e: print('done', e))
    time.sleep(23)
    await vc.disconnect()

@bot.command()
async def shortplay(ctx, member : discord.Member):
    channel = member.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio(source), after=lambda e: print('done', e))
    time.sleep(8)
    await vc.disconnect()


@bot.command()
async def playhere(ctx):
    channel = ctx.message.author.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio(source), after=lambda e: print('done', e))
    time.sleep(8)
    await vc.disconnect()


@bot.command()
async def info(ctx):
    await ctx.send('List of commands (ur a boomer if u dont know them lmao): \n')
    await ctx.send('.boomer(user, times - default = 1) \n .longplay(user) \n .shortplay(user) \n .playhere')

@bot.command()
async def addboomer(ctx, member : discord.Member):
    boomers.append(member)
    if member.nick:
        await ctx.send(f'Added {member.nick} to the boomer list.')
    else:
        await ctx.send(f'Added {member.name} to the boomer list.')

@bot.command()
async def getboomers(ctx):
    for boomer in boomers:
        if boomer.nick:
            await ctx.send(' - ' + boomer.nick + '\n')
        else:
            await ctx.send(' - ' + boomer.name + '\n')


@bot.event 
async def on_member_update(before, after): 
    if after.nick and  "boomer" in [role.name.lower() for role in before.roles]:
        await after.edit(nick = 'boomer')
        #current_time = datetime.datetime.now().strftime("%H:%M:%S")
        #log.write(f'A boomer : {before.name} got what they deserved on ' + str(current_time) + '\n')
        #log.flush()


@tasks.loop(seconds = 8)
async def change_status():
    await bot.change_presence(activity = discord.Game(next(statuses)))


bot.run(TOKEN)
