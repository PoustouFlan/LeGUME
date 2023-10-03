import discord
from discord.ext import commands, tasks
from discord import app_commands
from bot_utils import *

from data.models import *

import logging
log = logging.getLogger("LeGuMe")

class ActiveChallenges(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(
        name = "challenges",
        description = "liste les challenges actifs"
    )
    async def challenges(self, interaction) -> None:
        challenges = await Challenge.all().prefetch_related('category')

        if len(challenges) == 0:
            await interaction.response.send_message(
                "Aucun challenge actif en cours."
            )
            return

        await interaction.response.send_message("Liste des challenges actifs:")
        for challenge in challenges:
            await self.display_challenge(challenge)

    async def display_challenge(self, challenge) -> None:
        guild = self.bot.get_guild(GUILD_ID)
        channel = await guild.fetch_channel(CHANNEL_ID)
        await channel.send(str(challenge))


        ###
        return

        scoreboard = await Scoreboard.first()
        users = await scoreboard.users.all()

        embed = discord.Embed(
            title = challenge.name,
            colour = discord.Colour.red()
        )

        flags = 0
        value = ""
        for user in users:
            challenges = await user.solved_challenges.filter(
                name = challenge.name,
            )
            if len(challenges) > 0:
                value += (
                    f"[<@{user.id}>]\n"
                )
                flags += 1

        embed.add_field(
            inline = False,
            name = "",
            value = (
                f"{challenge.name}\n"
                f"{challenge.desc}\n"
                f":star: {challenge.points} ⠀ "
                f":triangular_flag_on_post: {flags}\n"
            )
        )

        embed.add_field(
            inline = False,
            name = "Flaggers",
            value = value,
        )

        await channel.send(
            embed = embed,
        )

async def setup(bot):
    await bot.add_cog(ActiveChallenges(bot), guilds = [guild_object])
