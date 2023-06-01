from __init__ import guild_id, Cache, Memoria
from metadata import changedatabase

import discord
from discord import app_commands
from discord.ext import commands

class Utils(commands.GroupCog, name = 'utils'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        super().__init__()

    @app_commands.command(name = 'verificar', description = 'Verificar a un usuario')
    @app_commands.describe(user = 'Usuario al cual verificar')
    async def verificar(self, interaction: discord.Interaction, user: discord.Member):
        changedatabase(Memoria, user.id, { 'verified': True })
        return await interaction.response.send_message(content = f'🟢 <@!{user.id}> verificado!', ephemeral = True)
    
    """@app_commands.command(name = 'rango', description = 'Poner un rango')
    @app_commands.describe(user = 'Usuario al cual poner el rango', rango = 'rango')
    async def rango(self, interaction: discord.Interaction, user: discord.Member, rango: discord.Role):
        print(commands.Cog.get_listeners(self))
        #changedatabase(Memoria, user.id, { 'rank': True })
        #return await interaction.response.send_message(content = f'🟢 <@!{user.id}> verificado!', ephemeral = True)"""

async def setup(bot: commands.Bot):
    await bot.add_cog(Utils(bot), guild = discord.Object(id = guild_id))        