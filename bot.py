#imports stuff needed for this code read dependencies.txt

import discord
import cogs
import os
import pretty_help
from pretty_help import PrettyHelp, Navigation
from discord.ext import commands


#this is the bot about embed
embed = discord.Embed(title="Bot About Page", colour=discord.Colour(0x3e038c))

embed.add_field(name=f"Made by", value="ping/dm = block (except friends) #7873 and Alexx #7687", inline=False)
embed.add_field(name=f"Bot Version:", value="1.4", inline=False)
embed.add_field(name=f"User Creation Time:", value="3/5/2021", inline=False)

#this is bot help commands and prefix (only 1 prefix is here might add more)
client = commands.Bot(command_prefix = "`", case_insensitive=True, help_command=PrettyHelp())

client.help_command = PrettyHelp(color=discord.Color.green(), no_category = 'commands', sort_commands = True, show_index = False, active_time = 60)


#this code is to send a text to let you know the bot is ready
@client.event
async def on_ready():
    print("Bot is ready")
#this is bots commands
@client.command()
async def whomademe(ctx):
    await ctx.send('Made by ping/dm = block (except friends) #7873 \nSome of this code is made by Alexx #7687 \nThis message will update to become embed instead of msg')

@client.command()
async def ping(ctx):
    await ctx.send(f'Bot Ping is {round(client.latency * 1000)} ms!')

@client.command()
async def easteregg(ctx):
    await ctx.send("this is not an easter egg its literally available in the help command")

@client.command()
async def test(ctx):
    await ctx.send("hello yes im alive :D")

@client.command()
async def about(ctx):
    await ctx.send(embed=embed)

@client.command()
async def rules(ctx):
    await ctx.send("#rules bruh read it im not rewriting it")

@client.command()
async def hello(ctx):
    await ctx.send("Hi")

@client.command()
async def hi(ctx):
    await ctx.send("Hello")

@client.command()
async def meme(ctx):
    await ctx.send("Unknown Command. Reason: Unreleased Command")

@client.command()
async def howtonotsleep(ctx):
    await ctx.send("1. Drink A Coffee (milk coffee works) :thumbsup: ")

@client.command()
@commands.has_permissions(manage_messages=True)
async def clearrecent(ctx, amount=2):
    await ctx.channel.purge(limit=amount)

@client.command()
@commands.has_any_role(799932791583146034, 800031646673534976)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
@commands.has_any_role(799932791583146034, 800031646673534976)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Not Enough Arguments. if this is a mistake contact bot administrator, or if you dont know any commands do `help')
#this is to see if cogs.py exist if doesnt prettyhelp (or the help command)will work but will not sorted by page
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')



client.run("NzU3MjkyOTM5NjQ2MDc0OTkx.X2eSAg.F9dUADfndubMdvNgAWUDeJBPj5A")