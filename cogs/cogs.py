# Main codes for cogs and other files in this Cogs folder
import discord
import cogs
from discord.ext import commands

class Example(commands.Cog, name='Example'):
    
    def __init__(self, client):
        self.client = client

        @commands.Cog.listener()
        async def on_ready(self):
            print('Bot is ready')
        
        @commands.command()
        async def ping(ctx):
            await ctx.send(f'Bot Ping is {round(client.latency * 1000)} ms!')


def setup(client):
    client.add_cog(Example(client))
