import discord
from discord.ext import commands
from discord import app_commands
from bot_utils import guild_object

import logging
log = logging.getLogger("LeGuMe")

from data.models import *

class FlagChallenge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = "flag",
        description = "soumet la solution d'un challenge"
    )
    async def flag(self, interaction, flag:str):
        user = await User.from_discord_user(interaction.user)

        flagged = await Challenge.filter(flag=flag).all()
        if len(flagged) == 0:
            await interaction.response.send_message(
                "Désolé, mais ce flag est incorrect.",
                ephemeral = True
            )
            return

        for challenge in flagged:
            # TODO: announce
            old_flags = await user.filter(solved_challenges__challenge=challenge).all()
            if len(old_flags) > 0:
                await interaction.response.send_message(
                    "Vous avez déjà résolu ce challenge...",
                    ephemeral = True,
                )
                return
            await user.add_flag(challenge)

        await interaction.response.send_message(
            "Flag correct!",
            ephemeral = True
        )

async def setup(bot):
    await bot.add_cog(FlagChallenge(bot), guilds = [guild_object])
