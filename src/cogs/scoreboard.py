import discord
from discord.ext import commands
from discord import app_commands
from bot_utils import guild_object

import logging
log = logging.getLogger("LeGuMe")

from data.models import *

import matplotlib.pyplot as plt
from datetime import date, timedelta

def create_plot(users, filename):
    plot_start = date.today() - timedelta(days = 200)
    for challenges, username in users:
        challenges.sort(key = lambda chal: chal[0])
        dates = []
        score = 0
        scores = []
        for chal_date, chal_points in challenges:
            score += chal_points
            if chal_date >= plot_start:
                dates.append(chal_date)
                dates.append(chal_date)
                scores.append(score - chal_points)
                scores.append(score)
        dates.append(date.today())
        scores.append(score)
        dates.insert(0, plot_start)
        scores.insert(0, scores[0])
        plt.plot(dates, scores, label=username)

    plt.grid(which='major', axis='y', color='gray', linestyle='dashed', linewidth=0.5, alpha=0.5)
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.gca().spines['bottom'].set_color('white')
    plt.gca().spines['left'].set_color('white')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.xticks(rotation=45)
    plt.tick_params(axis='x',colors='white')
    plt.tick_params(axis='y',colors='white')
    plt.legend(loc=(1.05, 0.25))
    plt.tight_layout()

    plt.savefig(filename, dpi=300, transparent=True)
    plt.close()

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = "scoreboard",
        description = "affiche le tableau des scores du serveur"
    )
    async def scoreboard(self, interaction):
        await interaction.response.defer()

        users = await User.all()
        for i, user in enumerate(users):
            users[i] = (await user.score(), user)

        users.sort(reverse = True)

        users_challenge = []

        embed = discord.Embed(
            colour = discord.Colour.blue()
        )

        digits = len(str(len(users)))

        for page in range((len(users) // 5) + 1):
            leaderboard = ""
            for i, (score, user) in enumerate(users[5*page:5*page + 5]):
                old_place = user.server_rank
                new_place = i + 1 + 5 * page
                user.server_rank = new_place
                await user.save()

                flags = await user.solved_challenges.all().prefetch_related("challenge")
                if page < 2:
                    users_challenge.append(
                        ([(flag.date, flag.challenge.points) for flag in flags],
                         user.id)
                    )
                if new_place < old_place:
                    emote = ":arrow_up_small:"
                elif new_place == old_place:
                    emote = ":black_large_square:"
                else:
                    emote = ":arrow_down_small:"

                score = str(score).ljust(5)
                flag_count = str(len(flags)).ljust(3)

                leaderboard += (
                    f"{emote} `{str(new_place).rjust(digits)}` | "
                    f":star: `{score}` ⠀ "
                    f":triangular_flag_on_post: `{flag_count}` | "
                    f"<@{user.id}>\n"
                )

            if page == 0:
                name = "Tableau des scores du serveur"
            else:
                name = ""

            embed.add_field(
                inline = False,
                name = name,
                value = leaderboard
            )

        create_plot(users_challenge, 'tmp/leaderboard.png')
        file = discord.File(
            'tmp/leaderboard.png',
            filename='leaderboard.png'
        )
        embed.set_image(url='attachment://leaderboard.png')

        await interaction.followup.send(
            "",
            file = file,
            embed = embed,
        )

async def setup(bot):
    await bot.add_cog(Leaderboard(bot), guilds = [guild_object])
