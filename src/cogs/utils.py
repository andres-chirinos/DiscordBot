from __init__ import guild_id, Cache

import discord
from discord import app_commands
from discord.ext import commands

class Utils(commands.GroupCog, name = 'utils'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        super().__init__()

    #List status
    """async def status_autocomplete(self, interaction: discord.Interaction, current: str):
        return [app_commands.Choice(name = "En linea", value = discord.Status.online),
                app_commands.Choice(name = "No molestar", value = discord.Status.do_not_disturb),
                app_commands.Choice(name = "Fuera de linea", value = discord.Status.offline),
                app_commands.Choice(name = "Idle", value = discord.Status.idle),
                app_commands.Choice(name = "Invisible", value = discord.Status.invisible)]
    
    @app_commands.command(name = 'status', description = 'Cambiar status')
    @app_commands.describe(status = 'Status')
    @app_commands.autocomplete(status = status_autocomplete)
    async def status(self, interaction: discord.Interaction, status):
        await self.bot.change_presence(status = status, activity = discord.Game(f"[{str(Cache.hget('appdata', 'prefix'))}] {str(Cache.hget('appdata', 'desc'))}"))"""

    #Mencionar al hacer una propuesta
    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        if thread.parent_id == int(Cache.hget('channels', 'parlamentforum_id')):
            await thread.send(content = f"🟢 <@&{int(Cache.hget('roles', 'deputy_id'))}>")
        elif thread.parent_id == int(Cache.hget('channels', 'marketforum_id')):
            await thread.send(content = f"🟢 <@&{int(Cache.hget('roles', 'trader_id'))}>")

async def setup(bot: commands.Bot):
    await bot.add_cog(Utils(bot), guild = discord.Object(id = guild_id))        