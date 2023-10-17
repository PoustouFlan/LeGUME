from typing import Optional, List

import discord
from discord import ui
from discord.ext import commands
from discord import app_commands
from bot_utils import guild_object

import logging
log = logging.getLogger("LeGuMe")

from data.models import *

class CreateCourseView(ui.View):
    name:       Optional[str]             = None
    challenges: Optional[List[Challenge]] = None

    @ui.select(
        placeholder = "Challenges présents",
        min_values = 0,
    )
    async def select_challenges(self, interaction, select) -> None:
        select.challenges = [
            await Challenge.filter(name = option).first()
            for option in select.values
        ]
        log.debug(select.challenges)

        course = await Course.create(
            name = self.name,
            active = True
        )
        await course.challenges.add(*select.challenges)

        await interaction.response.send_message(
            "Cours créé avec succès !"
        )

    def __init__(self, challenges, name) -> None:
        super().__init__()
        self.name = name
        self.select_challenges.options = [
            discord.SelectOption(label = challenge.name)
            for challenge in challenges
        ]
        self.select_challenges.max_values = min(10, len(challenges))



class CreateCourse(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(
        name = "create-course",
        description = "créée un nouveau cours"
    )
    async def create_course(self, interaction, name: str) -> None:
        all_challenges = await Challenge.all()
        view = CreateCourseView(all_challenges, name)

        await interaction.response.send_message(
            view = view
        )

async def setup(bot) -> None:
    await bot.add_cog(CreateCourse(bot), guilds = [guild_object])
