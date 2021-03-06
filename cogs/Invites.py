import discord
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import asyncio
import sqlite3
import datetime


async def send_wh2(url, whContent, whC2):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
        await webhook.send(embeds=[whContent, whC2], username='AND1558-Bot Logging', avatar_url='https://th.bing.com/th/id/Re4cba6bc5c9f26eb0494f3d689444a4f?rik=lry9hhilgkSv8A&riu=http%3a%2f%2fautomaticcrafters.com%2fwp-content%2fuploads%2f2020%2f06%2fnetherhero.jpg&ehk=MOSwxVYmsXSM%2fzQE63FOc%2fihBA8yG9rMoFS9L2Ls1m0%3d&risl=&pid=ImgRaw')

#I am using this because I want the bot to check if it has proper permissions before attemping to cache invites. 
# going to replace the try/except discord forbidden with perm checks
# 
# these functions belong to the discordutils lib
#
class InviteTracker(object):
    def __init__(self, client):
        self.client = client
        self._cache = {}
        
    async def cache_invites(self):
        for guild in self.client.guilds:
            self._cache[guild.id] = {}
            if guild.me.guild_permissions.manage_guild: #added perms check
                #print(f'{guild} cached')
                invs = await guild.invites()
                for invite in invs:
                    if invite.inviter not in self._cache[guild.id].keys():
                        self._cache[guild.id][invite.inviter] = []
                    self._cache[guild.id][invite.inviter].append(invite)

        
    async def update_invite_cache(self, invite):
        if invite.guild.me.guild_permissions.manage_guild: #added perms check
            if not invite.guild.id in self._cache.keys():
                self._cache[invite.guild.id] = {}
            if not invite.inviter in self._cache[invite.guild.id].keys():
                self._cache[invite.guild.id][invite.inviter] = []
            self._cache[invite.guild.id][invite.inviter].append(invite)

    async def remove_invite_cache(self, invite):
        for key in self._cache:
            for lists in self._cache[key]:
                user = self._cache[key][lists]
                if invite in user:
                    self._cache[key][lists].remove(invite)
                    break
                    
    async def remove_guild_cache(self, guild):
        if guild.id in self._cache.keys():
            del self._cache[guild.id]
                
    async def update_guild_cache(self, guild):
        if guild.me.guild_permissions.manage_guild: #added perms check
            invs = await guild.invites()
            self._cache[guild.id] = {}
            for invite in invs:
                if not invite.inviter in self._cache[guild.id].keys():
                    self._cache[guild.id][invite.inviter] = []
                self._cache[guild.id][invite.inviter].append(invite)
        
    async def fetch_inviter(self, member):
        invited_by = None
        invs = {}
        if member.guild.me.guild_permissions.manage_guild: #added permission check
            new_invites = await member.guild.invites()
        else:
            return None

        for invite in new_invites:
            if not invite.inviter in invs.keys():
                invs[invite.inviter] = []
            invs[invite.inviter].append(invite)
        for new_invite_key in invs:
            for cached_invite_key in self._cache[member.guild.id]:
                if new_invite_key == cached_invite_key:
                    new_invite_list = invs[new_invite_key]
                    cached_invite_list = self._cache[member.guild.id][cached_invite_key]
                    for new_invite in new_invite_list:
                        for old_invite in cached_invite_list:
                            if new_invite.code == old_invite.code and new_invite.uses-old_invite.uses >= 1:
                                cached_invite_list.remove(old_invite)
                                cached_invite_list.append(new_invite)
                                return new_invite_key



class Invites(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.tracker = InviteTracker(client)

        self.conn = sqlite3.connect('serverconfigs.db')
        self.c = self.conn.cursor()
        self.conn2 = sqlite3.connect('blacklists.db')
        self.c2 = self.conn2.cursor()

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(2)
        print('Starting to cache invites!')
        print('--------------------------')
        await self.tracker.cache_invites()
        print('--------------------------')
        print('Finished caching invites!')
        print('Bot is ready!')
        print(f"Servers - {str(len(self.client.guilds))}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await asyncio.sleep(1)

        god = guild.owner.id
        rows = self.c2.execute("SELECT user_id FROM userblacklist WHERE user_id = ?",(god,),).fetchall()
        if rows != []:
            await self.client.get_guild(int(guild.id)).leave()
            ch = self.client.get_channel(813600852576829470)
            
            embed = discord.Embed(colour=0xe74c3c)
            embed.set_author(name=f"Left guild with blacklisted owner")
            embed.add_field(name=(str(guild.name)), value=str(guild.id) + 
            "\n" + str(len(list(filter(lambda m: m.bot, guild.members)))) + " bots" + 
            "\n" + str(len(list(filter(lambda m: not m.bot, guild.members)))) + " humans" + 
            "\n" + "Created at " + str(guild.created_at), inline=False)
            embed.add_field(name='Server Owner', value=(f'{guild.owner} ({guild.owner.id})')) 
            embed.set_thumbnail(url=guild.icon_url)
            await ch.send(embed=embed)
            
            return

        
        rows = self.c2.execute("SELECT guild_id FROM guildblacklist WHERE guild_id = ?",(guild.id,),).fetchall()
        if rows != []:
            await self.client.get_guild(int(guild.id)).leave()
            ch = self.client.get_channel(813600852576829470)
            
            embed = discord.Embed(colour=0xe74c3c)
            embed.set_author(name=f"Left blacklisted guild")
            embed.add_field(name=(str(guild.name)), value=str(guild.id) + 
            "\n" + str(len(list(filter(lambda m: m.bot, guild.members)))) + " bots" + 
            "\n" + str(len(list(filter(lambda m: not m.bot, guild.members)))) + " humans" + 
            "\n" + "Created at " + str(guild.created_at), inline=False)
            embed.add_field(name='Server Owner', value=(f'{guild.owner} ({guild.owner.id})')) 
            embed.set_thumbnail(url=guild.icon_url)
            await ch.send(embed=embed)
            
            return
        
        else:
            await self.tracker.update_guild_cache(guild)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        await self.tracker.remove_invite_cache(invite)

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        await self.tracker.update_invite_cache(invite)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.tracker.remove_guild_cache(guild)

    @commands.Cog.listener()
    async def on_member_join(self, member):

        server = member.guild.id
        rows = self.c.execute("SELECT server_id, log_channel, whURL FROM logging WHERE server_id = ?",(server,),).fetchall()

        if rows != []:
            inviter = await self.tracker.fetch_inviter(member)  # inviter is the member who invited
            if inviter is None:
                embed = discord.Embed(color=0x000000)
                embed.set_author(name=f"{member}", icon_url=member.avatar_url)
                embed.title = f"Was invited" 
                embed.add_field(name='Inviter', value=f'???', inline = True)
                embed.add_field(name='Error', value=f'Bot does not have sufficient\n permissions to view invites \n or an error occurred', inline = True)
                #embed.add_field(name='Invite code used', value=f'{inviter}', inline = True)
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_footer(text=f'ID: {member.id}' + '\u200b')


                created_at = member.created_at.strftime("%b %d, %Y")
                embed1 = discord.Embed(color=0x00FF00)
                embed1.set_author(name=f"{member}", icon_url=member.avatar_url)
                embed1.title = f"Member joined" 
                embed1.description = f'Account created on {created_at}'
                embed1.timestamp = datetime.datetime.utcnow()
                embed1.set_footer(text=f'ID: {member.id}' + '\u200b')


            else:
            
                embed = discord.Embed(color=0x000000)
                embed.set_author(name=f"{member}", icon_url=member.avatar_url)
                embed.title = f"Was invited" 
                embed.add_field(name='Inviter', value=f'{inviter}', inline = True)
                #embed.add_field(name='Invite code used', value=f'{inviter}', inline = True)
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_footer(text=f'ID: {member.id}' + '\u200b')


                created_at = member.created_at.strftime("%b %d, %Y")
                embed1 = discord.Embed(color=0x00FF00)
                embed1.set_author(name=f"{member}", icon_url=member.avatar_url)
                embed1.title = f"Member joined" 
                embed1.description = f'Account created on {created_at}'
                embed1.timestamp = datetime.datetime.utcnow()
                embed1.set_footer(text=f'ID: {member.id}' + '\u200b')
            

            toprow = rows[0] 
            whURL = toprow[2]
            await send_wh2(whURL, embed1, embed) #sends both embeds in one message






def setup(client):
    client.add_cog(Invites(client))