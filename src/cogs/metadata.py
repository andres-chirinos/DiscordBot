from __init__ import guild_id, Cache
from memory import *

import discord, os, requests
from discord import app_commands
from discord.ext import commands


class Metadata(commands.GroupCog, name="metadata"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        super().__init__()

    @app_commands.command(name="verificar", description="Verificar a un usuario")
    @app_commands.describe(user="Usuario al cual verificar")
    async def verificar(self, interaction: discord.Interaction, user: discord.Member):
        await update_one(
            "master",
            str(user.id),
            {"type": "identification"},
            {"$set": {"verified": True}},
        )
        return await interaction.response.send_message(
            content=f"🟢 <@!{user.id}> verificado!", ephemeral=True
        )

    @app_commands.command(name="register", description="Register metadata")
    async def register(self, interaction: discord.Interaction):
        url = f"""https://discord.com/api/v10/applications/{os.environ.get("DISCORD_CLIENT_ID")}/role-connections/metadata"""
        data = json.loads(Cache.get("registermetadata"))

        response = requests.put(
            url,
            data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bot {os.environ.get('TOKEN')}",
            },
        )
        if response.ok:
            return await interaction.response.send_message(
                content=f"🟢 Metadata registrada!", ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Metadata(bot), guild=discord.Object(id=guild_id))
