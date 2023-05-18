import os
import discord, requests
from discord import app_commands
from discord.ext import commands, tasks
from __init__ import guild_id, Cache

import urllib.request, json

class Minecraft(commands.GroupCog, name = 'minecraft'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.getserverstatus.start()

        super().__init__()

    def get_server_info(self, ip:str):
        url = f'https://api.mcsrvstat.us/2/{ip}'
        response = requests.get(url)
        if response.ok:
            data = response.json()
            content = f"**IP. {ip}**\n"
            if data['online'] == True:
                if data.get('hostname'):
                    content = content + f"\n> Host. `{data['hostname']}`"
                if data.get('version'):
                    content = content + f"\n> Versión. `{data['version']}`"
                if data.get('players') and data['players']['max']:
                    content = content + f"\n> Jugadores. `{data['players']['online']}` de `{data['players']['max']}`"
                content = content + f"\n-> https://mcsrvstat.us/server/{ip}"
            else:
                content = content + "Offline"
            return content
        else:
            raise Exception(f'Error getting discord metadata: [{response.status_code}] {response.text}')
    
    @app_commands.command(name = 'status', description = 'Obtener el estatus de un server de minecraft')
    @app_commands.describe(ip = 'Ip del servidor')
    async def send(self, interaction: discord.Interaction, ip:str = Cache.hget('minecraft', 'serverip')):
        await interaction.response.send_message(content = f'🟢 {self.get_server_info(ip)}', ephemeral = True)

    #Revisar el estado del server.
    @tasks.loop(minutes=5)
    async def getserverstatus(self): 
        link = str(Cache.hget('messages', 'minecraft_status')).split('/')
        channel = self.bot.get_channel(int(link[-2]))
        message = await channel.fetch_message(int(link[-1]))
        await message.edit(content = f"{self.get_server_info(Cache.hget('minecraft', 'serverip'))}\nDynmap. {Cache.hget('minecraft', 'serverdynmap')}")
        
    @getserverstatus.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):  
    await bot.add_cog(Minecraft(bot), guild = discord.Object(id = guild_id))