import discord
import datetime
import asyncio
import cogs
from discord.ext import commands




class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            await guild.text_channels[0].send(f"Hello {guild.name}! I am {self.client.user.display_name}. Thank you for inviting me! \nTo see what commands I have available type `_help`\nMade by Alexx#7687")
            await guild.text_channels[0].send('https://cdn.discordapp.com/attachments/386995303066107907/533479547589623810/unknown.png')
        except:
            return

#################################################SHHHHHHHHHHH!

    @commands.cooldown(1, 3, commands.BucketType.channel)
    @commands.command()
    async def minty(self, ctx):

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        try:
            firstmessage = await ctx.send(f'{ctx.author.mention}, UWU! THIS IS A SECRET COMMAND! Enter anything to continue o.O')
            m1 = await self.client.wait_for('message', check=check, timeout=30)
            
        
            secondmessage = await ctx.send(f'{ctx.author.mention}, Minty is a cool person and friend UWUWU, they are a big supporter of the bot and for that I say thank u! :) \n Minty club invite code: V6y6WUB5vg')
            thirdmessage = await ctx.send('To delete these messages, enter anything into chat again.')
            m2 = await self.client.wait_for('message', check=check, timeout=120)
           
            

            await asyncio.sleep(1)
            await firstmessage.delete()
            await asyncio.sleep(1)
            await secondmessage.delete()
            await asyncio.sleep(1)
            await thirdmessage.delete()
            await asyncio.sleep(1)
            await ctx.message.delete()

        except asyncio.exceptions.TimeoutError:
            return await ctx.send(f'You did not reply in time :(')
    
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command()
    async def pong(self, ctx):
        await ctx.send(':thinking:')
        
def setup(client):
	client.add_cog(Events(client))