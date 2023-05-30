from __init__ import guild_id, Cache

import discord
from discord import app_commands
from discord.ext import commands

from cogs.register.passport import passport

class Register_modal(discord.ui.Modal):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.nick = discord.ui.TextInput(label = 'Nick de minecraft', placeholder = 'Steve', min_length = 3, max_length = 16, required = True)
        
        super().__init__(title = 'Registro', custom_id = 'register_modal', timeout = None)
        self.add_item(self.nick)

    async def on_submit(self, interaction: discord.Interaction):
        if not interaction.user.get_role(int(Cache.hget('roles', '@_id'))):
            role = interaction.user.guild.get_role(int(Cache.hget('roles', '@_id')))
            await interaction.user.edit(nick = str(self.nick), roles = [role], reason = 'Registro')
        else:
            await interaction.user.edit(nick = str(self.nick), reason = 'Actualización')
        return await interaction.response.send_message(content = '🟢', ephemeral = True, delete_after = 10)

class Register_view(discord.ui.View):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        super().__init__(timeout = None)

    @discord.ui.button(label = "Registrate!", style = discord.ButtonStyle.red, custom_id = 'register_button')
    async def register(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Register_modal(self.bot))

class Register(commands.GroupCog, name = 'register'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()
    
    #Para registrarse
    @app_commands.command(name = 'user', description = 'Registro manual')
    @app_commands.describe(user = 'Elija al usuario', nick = 'Ponga su nick')
    async def register(self, interaction: discord.Interaction, user: discord.Member, nick:str): 
        if not user.get_role(int(Cache.hget('roles', '@_id'))):
            role = interaction.user.guild.get_role(int(Cache.hget('roles', '@_id')))
            await user.edit(nick = str(nick), roles = [role], reason = 'Registro')
        else:
            await user.edit(nick = str(nick), reason = 'Actualización')
        return await interaction.response.send_message(content = '🟢', ephemeral = True, delete_after = 10)

    #Para poner boton de registro
    @app_commands.command(name = 'set', description = 'Poner boton de registro')
    async def registerbutton(self, interaction: discord.Interaction): 
        await interaction.channel.send(view = Register_view(self.bot))
        return await interaction.response.send_message(content = '🟢', ephemeral = True)
        
async def setup(bot: commands.Bot):
    bot.add_view(Register_view(bot))
    await bot.add_cog(Register(bot), guild = discord.Object(id = guild_id))        