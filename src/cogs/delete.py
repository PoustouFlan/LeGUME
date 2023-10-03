import discord
from discord.ext import commands
from discord import app_commands
from bot_utils import guild_object

import logging
log = logging.getLogger("LeGuMe")

from data.models import *

class Delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = "delete",
        description = "supprime toutes les données associées à votre compte Discord"
    )
    async def delete(self, interaction):
        # TODO: add option to delete other accounts if admin
        user = User.from_interaction(interaction)
        await user.delete()

        await interaction.response.send_message(
            "Toutes les données associées à votre compte ont été supprimées avec succès"
        )

async def setup(bot):
    await bot.add_cog(Delete(bot), guilds = [guild_object])
