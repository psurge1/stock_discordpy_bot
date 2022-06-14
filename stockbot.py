import discord # Discord API
from discord.ext import commands, tasks

import fmpsdk # Stock Data API (FmpCloud)

import requests, json

from matplotlib import pyplot as plt # Graphing tool
import numpy as np
import time

from utils.file_tools import txt_tools as txt_t # txt file reader

txt_tool=txt_t()

prefix='$'

client=commands.Bot(command_prefix=prefix)

client.remove_command("help")

green_status=True # variable determining bot status (odd or even)

status_list=["Bull", "Bear"]
list_value=3

# pfp2=open("img/stock2.png", 'rb').read() bot status pfps (currently not in use)
# pfp1=open("img/stock1.png", 'rb').read() bot status pfps (currently not in use)

apikey = txt_tool.read(txt_tool.read(r".\key.txt").split(sep='\n')[0])

credit = "Stock data provided by FmpCloud"

@client.event
async def on_ready():
    """
    function called when the bot is online
    """
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Stocks | $help"))
    # update.start()
    print (f"Bot is ready. \nDiscord.py {discord.__version__}")
    print (time.strftime("%H:%M:%S", time.localtime()))

@client.command(pass_context=True)
async def help(ctx, cmd=""):
    """
    custom help command
    """
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
    """
    updates stock discord bot's activity status (in development)
    """
    global green_status, list_value
    if green_status:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status_list[list_value%2]))
        # if status_list[list_value%2] == "Bull":
        #     # await client.user.edit(avatar=pfp1)
        # elif status_list[list_value%2] == "Bear":
        #     await client.user.edit(avatar=pfp2)
        # list_value+=1
    else:
        await client.change_presence(status=discord.Status.online, activity=discord.Game('Stocks'))
        # await client.user.edit(avatar=pfp1)

    # green_status = not green_status; # change

@client.command()
async def clear(ctx, amount=1):
    """
    clears images in the channel of the command
    """
    await ctx.channel.purge(limit=amount+1)

@client.command()
async def invite(ctx, password):
    """
    sends a bot invite link
    """
    if password == txt_tool.read(r".\invpass.txt"):
        await ctx.channel.purge(limit=1)
        await ctx.send('https://discord.com/api/oauth2/authorize?client_id=899382333843574845&permissions=2416438352&scope=bot')

@client.command()
async def greet(ctx):
    """
    in development
    """
    pass

@client.command()
async def check(ctx, a, b=''):
    t_years = 10
    t_months = 0
    t_days = 0
    """
    sends an embed with a given stock's data
    """
    a = a.upper()
    symbol: str = a
    stock_dict = fmpsdk.company_profile(apikey=apikey, symbol=symbol)[0]
    key_arr = list(stock_dict.keys())
    bad_arr = ['symbol', 'description']
    if b != '':
        if b in key_arr and b not in bad_arr:
            detail_embed=discord.Embed(
                title=camel_case_to_sentence(b),
                colour=discord.Colour.green()
            )
            detail_embed.add_field(name=a, value=stock_dict[b])
            detail_embed.set_footer(text=credit)

            await ctx.send(embed=detail_embed)
        else:
            await ctx.send(embed=discord.Embed(
                description="Detail not found",
                colour=discord.Colour.green()
            ))
    else:
        t_total_days = int(356.25*t_years+30.437*t_months+t_days)
        hist_stock_data = json.loads(requests.get(f"https://fmpcloud.io/api/v3/historical-price-full/{a}?timeseries={t_total_days}&apikey={apikey}").text)
        stock_embed=discord.Embed(
            title=a,
            description=stock_dict['companyName'],
            colour=discord.Colour.green()
        )
        stock_embed.set_footer(text=credit)

        for k in key_arr:
            if k not in bad_arr:
                stock_embed.add_field(name=camel_case_to_sentence(k), value=stock_dict[k], inline=True)
        
        # The following ill be completed once I can access historical stock data
        # open, high, low, close
        arr_time = []
        arr_open = []
        arr_high = []
        arr_low = []
        arr_close = []
        for i in range(len(hist_stock_data['historical'])-1, -1, -1):
            # print(hist_stock_data['historical'][i])
            arr_time.append(hist_stock_data['historical'][i]['date'])
            arr_open.append(hist_stock_data['historical'][i]['open'])
            arr_high.append(hist_stock_data['historical'][i]['high'])
            arr_low.append(hist_stock_data['historical'][i]['low'])
            arr_close.append(hist_stock_data['historical'][i]['close'])
        graph(a, arr_time, [arr_open, arr_high, arr_low, arr_close])
        
        image = discord.File(r"img\graph.png", filename="graph.png")
        stock_embed.set_image(url="attachment://graph.png")

        await ctx.send(file=image, embed=stock_embed)
            
        # future improvement: reactions allowing user to change time frame of stock graph
        # stock_msg = await ctx.send(file=image, embed=stock_embed)
        # for r_e in ('🆈', '🅈', '🅼', '🄼', '🅳', '🄳'):
        #     await ctx.add_reaction(stock_msg, r_e)

def graph(stock_label, x_arr, y_matrix, xtitle=None, ytitle=None, labels=['open', 'high', 'low', 'close'], colors=['r', 'g', 'b', 'c', 'm', 'y', 'w', 'k']):
    """
    plots a graph using matplotlib and saves it to img/graph.png
    """
    # dev_x_one=[25,26,27,28,29,30,31,32,33,34,35]
    # dev_y_one=[384, 420, 467, 493, 532, 560, 623, 649, 673, 687, 737]
    # dev_x_two=[]
    # dev_y_two=[]
    # # dev_x_two=[25,26,27,28,29,30,31,32,33,34,35]
    # # dev_y_two=[747, 687, 673, 649, 623, 560, 532, 493, 467, 420, 384]
    # for i in range(len(dev_x_one)):
    #     dev_x_two.append(dev_x_one[i]+5)
    #     dev_y_two.append(dev_y_one[i]*2)

    plt.figure(facecolor='None')
    
    fig = plt.figure()
    
    ax = fig.add_subplot(111)

    fig.patch.set_facecolor('None')

    for i in range(len(y_matrix)):
        ax.plot(x_arr, y_matrix[i], color=colors[i%len(colors)], label=labels[i%len(labels)])

    ax.set_title(stock_label, color='white', fontsize=20, fontweight='bold')
    
    for a in (xtitle, ytitle):
        if a!=None:
            ax.set_ylabel(a, fontsize=12, fontweight='bold')

    for b in ['bottom', 'top', 'left', 'right']:
        ax.spines[b].set_color('white')
    
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.set_ticks([x_arr[0], x_arr[int(len(x_arr)/3)], x_arr[int(len(x_arr)*2/3)], x_arr[-1]])
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.set_facecolor('None')

    ax.legend()

    plt.savefig(r"img\graph.png", dpi=100)

    mm = np.poly1d(x_arr, y_matrix[3], 3)
    # m_line = np.linspace(1, 22, 100)

    plt.plot(mm(x_arr))

    plt.savefig(r"img\simplification.png", dpi=100)
    plt.close()

# The following commands are either in development or are ideas for future commands
# @client.command
# async def error(ctx, text):
#     """
#     displays a universal error message as an embed
#     """
#     await ctx.send(embed=discord.Embed(
#                 description=text,
#                 colour=discord.Colour.green()
#             ))

def camel_case_to_sentence(s):
    r = ""
    r += s[0].upper()
    for i in range(1, len(s)):
        if s[i].isupper():
            r += " "
        r += s[i]
    return r

@client.command()
async def code(ctx, *, arg):
    """
    executes and returns python code with syntax highlighting in discord
    """
    w=0
    raw_code=""
    while True:
        if w==len(arg) or arg[w]==prefix:
            break
        elif arg[w] == '?' and arg[w+2] == '?':
            p = arg[w+1]
            if p == 't':
                raw_code+='    '
            elif p == 's':
                raw_code+=' '
            w+=3
        else:
            raw_code+=arg[w]
            w+=1

    # exec(raw_code)
    await ctx.send(f"```py\n{raw_code}\n```")

client.run(txt_tool.read(r".\token.txt"))