# Admins.py
import contextlib
import io
import textwrap
from traceback import format_exception
import asyncio
import discord
import sqlite3
from discord.ext import commands
from discord.ext.commands.core import bot_has_permissions

BOT_ID = int(752585938630082641)
OWNER_ID = int(247932598599417866)

def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content

from discord.ext.buttons import Paginator


class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass

#Owner Category
class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.conn = sqlite3.connect('blacklists.db')
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS userblacklist(user_id INTERGER)")
        self.c.execute("CREATE TABLE IF NOT EXISTS guildblacklist(guild_id INTERGER)")
        print(f'Connected to the blacklist db! {self.conn.total_changes}')


    #gets current servers the bot is in
    @commands.command()
    @commands.is_owner()
    async def listguilds(self, ctx):
        servers = self.client.guilds
        for guild in servers:
            embed = discord.Embed(colour=0x7289DA)
            embed.set_footer(text=f"Guild requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            embed.add_field(name=(str(guild.name)), value=str(guild.id) + 
            "\n" + str(len(list(filter(lambda m: m.bot, guild.members)))) + " bots" + 
            "\n" + str(len(list(filter(lambda m: not m.bot, guild.members)))) + " humans" + 
            "\n" + "Created at " + str(guild.created_at), inline=False)
            embed.add_field(name='Server Owner', value=(f'{guild.owner} ({guild.owner.id})')) 
            embed.set_thumbnail(url=guild.icon_url)
            
            await ctx.send(embed=embed)
            await asyncio.sleep(1)

    #makes the bot leave the given server ID
    @commands.command()
    @commands.is_owner()
    async def leaveguild(self, ctx, serverid:int):
        try:
            await ctx.send(f'Left server with ID of `{serverid}` ✅')
            await self.client.get_guild(int(serverid)).leave()
        except:
            await ctx.send('An error occured.', delete_after=5.0)

    #owner only command to change the status of the bot
    @commands.command()
    @commands.is_owner()
    async def status(self, ctx,* ,status):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(f'{status}'))
        await ctx.send(f'Changed bot status to **{status}** ! ✅ ', delete_after=5.0)

    
    #simple say command to make the bot say something. Owner only atm
    @commands.command()
    @commands.is_owner()
    async def say(self, ctx,* ,args):
        mesg = ''.join(args)
        await ctx.message.delete()
        return await ctx.send(mesg)
    
    #renames a channel
    @commands.command(hidden=True)
    @commands.is_owner()
    async def rc(self, ctx, *, new_name):
        try:
            channel = ctx.message.channel
            await channel.edit(name=new_name)
            await ctx.send(f'Changed channel name to **{new_name}** ! ✅ ', delete_after=5.0)
        except:
            await ctx.send('An error occured.', delete_after=5.0)
    
    #deletes a channel
    @commands.command(hidden=True)
    @commands.is_owner()
    async def dc(self, ctx):
        try:
            await ctx.message.channel.delete()
        except:
            await ctx.send('An error occured.', delete_after=5.0)
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def cc(self, ctx,*, name):
        try:
            await ctx.guild.create_text_channel(name)
        except:
            await ctx.send('An error occured.', delete_after=5.0)

    @commands.command()
    @commands.is_owner()
    async def listperms(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.message.author
        perm_list = [perm[0] for perm in member.guild_permissions if perm[1]]
        await ctx.send(perm_list)

    #bans a user
    @bot_has_permissions(ban_members=True)
    @commands.is_owner()    
    @commands.command(hidden=True)
    async def bean(self, ctx, user: discord.User,*, reason=None):
        if ctx.message.author.id == user.id: #checks to see if you are banning yourself
            return await ctx.send(f'{ctx.author.mention} you cannot ban yourself, silly human! `>.<`')
        if user.id == BOT_ID:
            return await ctx.send(f'{ctx.author.mention} you cannot ban me with my own commands! SMH.')

        try:
            await ctx.guild.ban(user, reason=f"By {ctx.author} for {reason}")
            await ctx.send(f'{user.mention} was banned! `>:(`')
        except:
            return await ctx.send("Could not ban this user.")


    # @commands.Cog.listener()
    # async def on_guild_join(self, guild):

    # has been moved to invitetracker to use the on_guild_join event there so the databases are only accessed once per join


    
    @commands.command()
    @commands.is_owner()
    async def adduser(self, ctx, user: discord.User):
        userid = str(user.id)
        self.c.execute("INSERT INTO userblacklist VALUES(?)", (userid,))
        self.conn.commit()
        await ctx.send(f'User with id of `{user.id}` was blacklisted ✅')

    @commands.command()
    @commands.is_owner()
    async def removeuser(self, ctx, user: discord.User):
        userid = str(user.id)
        self.c.execute("DELETE FROM userblacklist WHERE user_id = ?",(userid,))
        self.conn.commit()
        await ctx.send(f'User with id of `{user.id}` was removed from the blacklist ✅')

    @commands.command()
    @commands.is_owner()
    async def checkuser(self, ctx, user: discord.User):
        rows = self.c.execute("SELECT user_id FROM userblacklist WHERE user_id = ?",(user.id,),).fetchall()
        if rows == []:
            return await ctx.send(f'User with id of `{user.id}` was `NOT` found in the blacklist.')
        if rows != []:
            return await ctx.send(f'User with id of `{user.id}` `was found` in the blacklist.')
        
    @commands.command()
    @commands.is_owner()
    async def addguild(self, ctx, guild:int):
        guildID = str(guild)
        self.c.execute("INSERT INTO guildblacklist VALUES(?)", (guildID,))
        self.conn.commit()
        await ctx.send(f'Guild with id of `{guild}` was blacklisted ✅')

    @commands.command()
    @commands.is_owner()
    async def removeguild(self, ctx, guild:int):
        guildID = str(guild)
        self.c.execute("DELETE FROM guildblacklist WHERE guild_id = ?",(guildID,))
        self.conn.commit()
        await ctx.send(f'Guild with id of `{guild}` was removed from the blacklist ✅')

    @commands.command()
    @commands.is_owner()
    async def checkguild(self, ctx, guild:int):
        guildID = str(guild)
        rows = self.c.execute("SELECT guild_id FROM guildblacklist WHERE guild_id = ?",(guildID,),).fetchall()
        if rows == []:
            return await ctx.send(f'Guild with id of `{guild}` was `NOT` found in the blacklist.')
        if rows != []:
            return await ctx.send(f'Guild with id of `{guild}` `was found` in the blacklist.')




    @commands.command(name="eval")
    @commands.is_owner()
    async def _eval(self, ctx, *, code):
        code = clean_code(code)

        local_variables = {
            "discord": discord,
            "commands": commands,
            "client": self.client,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message
        }

        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
                )

                obj = await local_variables["func"]()
                result = f"{stdout.getvalue()}\n-- {obj}\n"
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))

        pager = Pag(
            timeout=100,
            entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
            length=1,
            prefix="```py\n",
            suffix="```"
        )

        await pager.start(ctx)

def setup(client):
    client.add_cog(Admin(client))


