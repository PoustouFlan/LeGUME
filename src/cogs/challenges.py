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
        courses = await Course.all()
        if len(courses) == 0:
            await interaction.response.send_message("Pas de cours actif!")
            return

        await interaction.response.pong()
        for course in courses:
            await self.display_course(course)

    async def display_course(self, course):
        embed = discord.Embed(
            title = f"{course.name}",
            colour = discord.Colour.orange()
        )

        challenges = await course.challenges.all().prefetch_related('category')
        for challenge in challenges:
            embed.add_field(
                name = f"{challenge.name}",
                inline = False,
                value = (
                    f"**{challenge.category.name}**\n"
                    f":star: {challenge.points}\n"
                    f"{challenge.desc}\n"
                )
            )


        guild = self.bot.get_guild(GUILD_ID)
        channel = await guild.fetch_channel(CHANNEL_ID)
        await channel.send(
            embed = embed,
        )

async def setup(bot):
    await bot.add_cog(ActiveChallenges(bot), guilds = [guild_object])
