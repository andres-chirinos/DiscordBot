import discord, requests
from discord import app_commands
from discord.ext import commands, tasks
from __init__ import guild_id, Cache

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
            content = str()
            for i in data:
                if i == 'ip' or i == 'port' or i == 'version' or i == 'online' or i == 'hostname' or i == 'software':
                    content = f'{content}\n**{i}.** `{data[i]}`'
                elif i == 'motd':
                    content = f"{content}\n**{i}.** {data[i]['clean'][0]}"
                elif i == 'players':
                    content = f"{content}\n**{i}.** {data[i]['online']}/{data[i]['max']}"
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