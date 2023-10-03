import discord
from discord.ext import commands
from discord import app_commands
from bot_utils import *

import logging
log = logging.getLogger("LeGuMe")

from data.models import *

import matplotlib.pyplot as plt


def create_plot(flags, filename):
    dates = []
    score = 0
    scores = []
    for flag in flags[::-1]:
        dates.append(flag.date)
        scores.append(score)
        score += flag.challenge.points
        dates.append(flag.date)
        scores.append(score)

    plt.grid(which='major', axis='y', color='gray', linestyle='dashed', linewidth=0.5, alpha=0.5)
    plt.plot(dates, scores, color='gold')
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.gca().spines['bottom'].set_color('white')
    plt.gca().spines['left'].set_color('white')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.xticks(rotation=45)
    plt.tick_params(axis='x',colors='white')
    plt.tick_params(axis='y',colors='white')
    plt.tight_layout()

    plt.savefig(filename, dpi=300, transparent=True)
    plt.close()

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = "user-info",
        description = "affiche les informations d'un utilisateur"
    )
    async def user_info(self, interaction, user:discord.Member|None):
        await interaction.response.defer()
        if user is None:
            username = interaction.user.display_name
            avatar_url = interaction.user.display_avatar.url
            user = await User.from_discord_user(interaction.user)
        else:
            username = user.display_name
            avatar_url = user.display_avatar.url
            user = await User.from_discord_user(user)
        score = await user.score()

        embed = discord.Embed(
            title = f"Profil de {username}",
            colour = discord.Colour.orange()
        )
        embed.set_thumbnail(url=avatar_url)

        last_flags = ""
        flags = await user.solved_challenges.all().prefetch_related("challenge")

        for flag in flags[:5]:
            challenge = flag.challenge
            last_flags += f":star: {challenge.points} | {challenge.name}\n"

        filename = f"tmp/{user.id}_plot.png"
        create_plot(flags, filename)
        file = discord.File(filename, filename = filename[4:])
        embed.set_image(url = f"attachment://{filename[4:]}")

        embed.add_field(
            name = "Statistiques",
            inline = False,
            value = (
                f":star: {score} ⠀ "
                f":triangular_flag_on_post: {len(flags)}\n"
                #(":drop_of_blood:" * user.first_bloods) +
                #("\n" * (user.first_bloods > 0)) +
                #tr("level", level=user.level) +
                #tr("rank", rank=user.rank, count=user.user_count)
            )
        )

        embed.add_field(
            inline = False,
            name = "Derniers flags",
            value = last_flags
        )

        category_solves = ""
        categories = await Category.all()
        solved_per_category = {category.name: 0 for category in categories}
        for flag in flags:
            category = await flag.challenge.category.get()
            solved_per_category[category.name] += 1

        for category in categories:
            challenges = await category.challenges.all()
            total = len(challenges)
            solved = solved_per_category[category.name]

            bars = int(10 * (1 if total == 0 else solved / total))
            bar = "▰"*bars + "▱"*(10 - bars)
            star = ":star2:" if solved == total else ":black_large_square:"
            category_solves += f"{star} {bar} {category.name}: {solved} / {total}\n"

        embed.add_field(
            inline = False,
            name = "Catégories",
            value = category_solves
        )

        await interaction.followup.send(
            "",
            file = file,
            embed = embed,
        )

async def setup(bot):
    await bot.add_cog(UserInfo(bot), guilds = [guild_object])
