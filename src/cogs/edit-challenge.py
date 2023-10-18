import discord
from discord import ui
from discord.ext import commands
from discord import app_commands
from bot_utils import guild_object

import logging
log = logging.getLogger("LeGuMe")

from data.models import *

class EditChallengeModal(ui.Modal, title = "Édition du Challenge"):
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

    def __init__(self, challenge):
        super().__init__()
        self.name.placeholder = challenge.name
        self.category.placeholder = challenge.category.name
        self.points.placeholder = str(challenge.points)
        self.description.placeholder = challenge.desc
        self.flag.placeholder = challenge.flag
        self.challenge = challenge

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

        existing = await Challenge.filter(name = self.name.value).first()
        if existing is not None and existing != self.challenge:
            await interaction.response.send_message(
                "Un autre challenge du même nom existe déjà"
            )
            return

        self.challenge.name = self.name.value
        self.challenge.points = points
        self.challenge.category = category
        self.challenge.desc = self.description.value
        self.challenge.flag = self.flag.value
        await self.challenge.save()

        await interaction.response.send_message(
            "Le challenge a été édité avec succès"
        )

class Edit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = "edit",
        description = "Édite un challenge existant"
    )
    async def edit(self, interaction, name: str):
        challenge = await Challenge.filter(name = name).prefetch_related('category').first()
        if challenge is None:
            await interaction.response.send_message(
                f"Le challenge {name} n'existe pas"
            )
            return

        modal = EditChallengeModal(challenge)
        await interaction.response.send_modal(modal)

async def setup(bot):
    await bot.add_cog(Edit(bot), guilds = [guild_object])
