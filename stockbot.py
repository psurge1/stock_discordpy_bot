from typing_extensions import runtime
import discord
from discord.ext import commands, tasks

from utils import file_manager
from utils.file_tools import csv_tools as csv_manipulator
from utils.file_tools import txt_tools as txt_manipulator

prefix = "$"

client = commands.Bot(command_prefix = prefix)

# client.remove_command('help')

channel_id = 0
r = 1

status_list = ['Bull', 'Bear']
list_value = 0

csv_tool = csv_manipulator('./data/data.csv')
txt_tool = txt_manipulator()

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Stocks'))
    update.start()
    print (f"Bot is ready. \nDiscord.py {discord.__version__}")
'''
@client.command(pass_context=True)
async def help():
    author = ctx.message.author
'''
@tasks.loop(seconds=30)
async def update():
    global r
    if r%2==0:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status_list[list_value]))
    else:
        await client.change_presence(status=discord.Status.online, activity=discord.Game('Stocks'))
    r+=1

@client.command()
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount+1)

@client.command()
async def invite(ctx):
    await ctx.send('https://discord.com/api/oauth2/authorize?client_id=899382333843574845&permissions=2416438352&scope=bot')



@client.command()
async def greet(ctx):
    global channel_id
    await ctx.send('hi')
    ctx.message.guild.create_text_channel(f'trade channel-{channel_id}')
    channel_id+=1

@client.command()
async def buy(ctx, stock_label):
    await ctx.send(stock_label)

@client.command()
async def sell(ctx, stock_label):
    await ctx.send(stock_label)

@client.command()
async def check(ctx, stock_label):
    # embed with graph and data
    await ctx.send(stock_label)

@client.command()
async def graph(ctx, stock_label):
    await ctx.send(stock_label)

@client.command()
async def code(ctx, *, arg):
    w=0
    raw_code=""
    while True:
        if w==len(arg) or arg[w]==prefix:
            break
        raw_code+=arg[w]
        w+=1
    a = arg.split("\n")
    await ctx.send(raw_code)

# @client.command()
# async def run_script(ctx):
#     await ctx.send("hi")

# @client.command()
# async def append_app(ctx):
#     await ctx.send("hi")

# @client.command()
# async def delete_app(ctx, app_name):
#     #check if app exists and find its object
#     if (ctx.message.author.name == app.author): #if ctx author == App author
#         # show embed to confirm delete
#         # enter passkey to delete
#         # delete
#         print("todo: deleteApp command")



client.run(txt_tool.read('./token.txt'))