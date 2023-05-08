from __init__ import guild_id, Cache

import discord
from discord import app_commands
from discord.ext import commands

class Goverment(commands.GroupCog, name = 'goverment'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        super().__init__()

    #Mencionar al hacer una propuesta
    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        if thread.parent_id == int(Cache.hget('channels', 'parlamentforum_id')):
            await thread.send(content = f"🟢 <@&{int(Cache.hget('roles', 'deputy_id'))}>")
        elif thread.parent_id == int(Cache.hget('channels', 'marketforum_id')):
            await thread.send(content = f"🟢 <@&{int(Cache.hget('roles', 'trader_id'))}>")

async def setup(bot: commands.Bot):
    await bot.add_cog(Goverment(bot), guild = discord.Object(id = guild_id))        