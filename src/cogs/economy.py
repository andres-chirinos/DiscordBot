import discord
from discord import app_commands
from discord.ext import commands
from __init__ import guild_id, Memoria

class Economy(commands.GroupCog, name = 'economy'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.table = Memoria['master']['finance']
        
        super().__init__()

    def get_account(self, id):
        account = self.table.find_one({'_id':id})
        if account:
            return account
        else:
            return self.table.insert_one("""{
            "_id": {
                "$numberLong": {0}
            },
            "balance": 0,
            "suscriptions": [],
            "history": []
            }""".format(id))
        
    @app_commands.command(name = 'info', description = 'Información de la cuenta')
    async def balance(self, interaction: discord.Interaction):
        self.get_account(interaction.user.id)

async def setup(bot: commands.Bot):   
    await bot.add_cog(Economy(bot), guild = discord.Object(id = guild_id))