from tkinter import font
import discord
from discord.ext import commands, tasks

from matplotlib import pyplot as plt
import time

from utils import file_manager, data_cleaner
from utils.file_tools import csv_tools as csv_manipulator, txt_tools as txt_manipulator

prefix="$"

client=commands.Bot(command_prefix=prefix)

client.remove_command('help')

r=1

status_list=['Bull', 'Bear']
list_value=3

pfp1=open("img/stock1.png", 'rb').read()
pfp2=open("img/stock2.png", 'rb').read()

csv_tool=csv_manipulator()
txt_tool=txt_manipulator()

csv_tool.set_read_return_type('DICTDICT')
dataset=csv_tool.read(r"data\nasdaq_screener_1640713211469.csv")
# print(data_cleaner.list_dict_cleaner(dataset))

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Stocks | $help'))
    # update.start()
    print (f"Bot is ready. \nDiscord.py {discord.__version__}")
    print (time.strftime("%H:%M:%S", time.localtime()))

@client.command(pass_context=True)
async def help(ctx, cmd=""):
    help_embed=discord.Embed(
        title="Help",
        description="Type ``$help [command]`` for more info on a command",
        colour=discord.Colour.green()
    )

    help_embed.add_field(name="General", value=f"`` clear \n greet \n graph \n code ``", inline=True)
    help_embed.add_field(name="General", value=f"`` clear \n greet \n graph \n code ``", inline=True)

    await ctx.send(embed=help_embed)

@tasks.loop(seconds=30)
async def update():
    global r, list_value
    if r%2==0:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status_list[list_value%2]))
        # if status_list[list_value%2] == "Bull":
        #     # await client.user.edit(avatar=pfp1)
        # elif status_list[list_value%2] == "Bear":
        #     await client.user.edit(avatar=pfp2)
        # list_value+=1
    else:
        await client.change_presence(status=discord.Status.online, activity=discord.Game('Stocks'))
        # await client.user.edit(avatar=pfp1)
    r+=2; """change"""

@client.command()
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount+1)

@client.command()
async def invite(ctx, password):
    if password == txt_tool.read('./invpass.txt'):
        await ctx.channel.purge(limit=1)
        await ctx.send('https://discord.com/api/oauth2/authorize?client_id=899382333843574845&permissions=2416438352&scope=bot')

@client.command()
async def greet(ctx):
    print("DM")

@client.command()
async def check(ctx, a, b=''):
    # embed with graph and data
    b=b.upper()
    a=a.title()
    if b in dataset.keys():
        a="IPO Year" if a=="Ipo" else a
        if a in dataset[b].keys():
            detail_embed=discord.Embed(
                title=b,
                colour=discord.Colour.green()
            )
            detail_embed.add_field(name=a, value=dataset[b][a])
            detail_embed.set_footer(text="Stock data provided by nasdaq.com")

            await ctx.send(embed=detail_embed)

        else:
            await ctx.send(embed=discord.Embed(
                description="Detail not found",
                colour=discord.Colour.green()
            ))
    elif a.upper() in dataset.keys():
        a=a.upper()
        stock_embed=discord.Embed(
            title=a,
            description=dataset[a]['Name'],
            colour=discord.Colour.green()
        )
        stock_embed.set_footer(text=f"Stock data provided by nasdaq.com")

        n=1
        for k in dataset[a]:
            if n>1:
                stock_embed.add_field(name=k, value=dataset[a][k], inline=True)
            n+=1
        
        graph(a)
        image = discord.File(r"img\graph.png", filename="graph.png")
        stock_embed.set_image(url="attachment://graph.png")
        
        await ctx.send(file=image, embed=stock_embed)

    else:
        await ctx.send(embed=discord.Embed(
                description="Invalid stock symbol",
                colour=discord.Colour.green()
            ))

# @client.command
# async def error(ctx, text):
#     await ctx.send(embed=discord.Embed(
#                 description=text,
#                 colour=discord.Colour.green()
#             ))

@client.command()
async def define(ctx, *, arg):
    return lambda x, y: x * y

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

def graph(stock_label, xtitle=None, ytitle=None):
    dev_x_one=[25,26,27,28,29,30,31,32,33,34,35]
    dev_y_one=[384, 420, 467, 493, 532, 560, 623, 649, 673, 687, 737]
    dev_x_two=[]
    dev_y_two=[]
    for i in range(len(dev_x_one)):
        dev_x_two.append(dev_x_one[i]+5)
        dev_y_two.append(dev_y_one[i]*2)

    plt.figure(facecolor='None')
    
    fig = plt.figure()
    
    ax = fig.add_subplot(111)

    fig.patch.set_facecolor('None')

    ax.plot(dev_x_one, dev_y_one, color='b', label='One')
    ax.plot(dev_x_two, dev_y_two, color='r', label='Two')

    # ax.set_title(stock_label, color='white', fontsize=20, fontweight='bold')
    for a in (xtitle, ytitle):
        if a!=None:
            ax.set_ylabel(a, fontsize=12, fontweight='bold')

    for b in ['bottom', 'top', 'left', 'right']:
        ax.spines[b].set_color('white')
    
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.set_facecolor('None')

    ax.legend()

    plt.savefig(r"img\graph.png", dpi=100)
    plt.close()

client.run(txt_tool.read('./token.txt'))