import discord
from discord.ext import commands, tasks

from utils import file_manager, data_cleaner
from utils.file_tools import csv_tools as csv_manipulator, txt_tools as txt_manipulator

prefix="$"

client=commands.Bot(command_prefix=prefix)

# client.remove_command('help')

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
    global r, list_value
    if r%2==0:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status_list[list_value%2]))
        if status_list[list_value%2] == "Bull":
            await client.user.edit(avatar=pfp1)
        elif status_list[list_value%2] == "Bear":
            await client.user.edit(avatar=pfp2)
        list_value+=1
    else:
        await client.change_presence(status=discord.Status.online, activity=discord.Game('Stocks'))
        await client.user.edit(avatar=pfp1)
    r+=1; """change"""

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
async def check(ctx, stock_label):
    # embed with graph and data
    uppercase_stock_label=stock_label.upper()
    if (stock_label.upper() in dataset.keys()):
        stock_embed=discord.Embed(
            title=uppercase_stock_label,
            description=dataset[uppercase_stock_label]["Name"],
            colour=discord.Colour.green()
        )
        stock_embed.set_footer(text="Stock data provided by google.com and nasdaq.com")
        # stock_embed.set_image(url="")
        stock_embed.add_field(name="Source", value=f"https://www.google.com/search?q={stock_label.lower()}")
        
        await ctx.send(embed=stock_embed)
    else:
        await ctx.send("Invalid stock symbol")

@client.command()
async def embed(ctx):
    stock_embed = discord.Embed(
        title="Title",
        description="Description",
        colour=discord.Colour.blue()
    )
    stock_embed.set_footer(text="Footer")
    # embed.set_image(url="")
    # embed.set_thumbnail(url="")
    stock_embed.set_author(name="author")
    # embed.set_author(name="author", icon_url="")

    stock_embed.add_field(name="Field Text", value="Field Value", inline=True)
    stock_embed.add_field(name="Field Text", value="Field Value", inline=True)
    stock_embed.add_field(name="Field Text", value="Field Value", inline=False)

    await ctx.send(embed=stock_embed)

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