import discord
from discord import ui
from discord.ext import commands
from discord import app_commands
from bot_utils import guild_object

import logging
log = logging.getLogger("LeGuMe")

from data.models import *

class CreateChallengeModal(ui.Modal, title = "Sujet du cours"):
    name = ui.TextInput(
        label = "Nom",
        style = discord.TextStyle.short,
        placeholder = "Titre du Challenge",
        required = True,
        min_length = 1,
        max_length = 255,
    )
    category = ui.TextInput(
        label = "Catégorie",
        style = discord.TextStyle.short,
        placeholder = "Forensics",
        required = True,
        min_length = 1,
        max_length = 255,
    )
    points = ui.TextInput(
        label = "Score",
        style = discord.TextStyle.short,
        placeholder = "42",
        required = True,
        min_length = 1,
        max_length = 4,
    )
    description = ui.TextInput(
        label = "Description",
        style = discord.TextStyle.paragraph,
        placeholder = "Écrivez la description du challenge ici",
        required = True,
        min_length = 1,
        max_length = 4000,
    )
    flag = ui.TextInput(
        label = "Flag",
        style = discord.TextStyle.short,
        placeholder = "HDFR{What a Flag!}",
        required = True,
        min_length = 6,
        max_length = 255,
    )

    async def on_submit(self, interaction):
        try:
            points = int(self.points.value)
            category = await Category.filter(
                        name = self.category.value.lower()
                    ).first()
            if category is None:
                log.debug("La catégorie n'existe pas")
                raise ValueError

        except ValueError:
            return

        existing = await Challenge.filter(name = self.name.value).get()
        if existing is not None:
            await interaction.response.send_message(
                "Un challenge du même nom existe déjà"
            )
            return

        challenge = await Challenge.create(
            name = self.name.value,
            points = points,
            category = category,
            desc = self.description.value,
            flag = self.flag.value,
        )
        await interaction.response.send_message(
            "Le challenge a été créé avec succès"
        )

class Create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = "create",
        description = "créée un nouveau challenge"
    )
    async def create(self, interaction):

        modal = CreateChallengeModal()
        await interaction.response.send_modal(modal)

async def setup(bot):
    await bot.add_cog(Create(bot), guilds = [guild_object])
