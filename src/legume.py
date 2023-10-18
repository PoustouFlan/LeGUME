import discord
from discord.utils import setup_logging
import asyncio
from bot_utils import *
from discord.ext import commands

import logging
setup_logging()
log = logging.getLogger("LeGuMe")
log.setLevel(logging.DEBUG)

from data.db_init import init
from data.models import *

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix = "$ ",
    help_command = None,
    intents = intents
)

initial_extensions = [
    "cogs.user-info",
    # "cogs.announce",
    "cogs.create-challenge",
    "cogs.edit-challenge",
    "cogs.create-course",
    "cogs.delete",
    "cogs.scoreboard",
    "cogs.challenges",
    "cogs.flag",
]

@bot.event
async def on_ready():
    log.info(f"Connecté en tant que {bot.user}")
    commands = await bot.tree.sync(guild = guild_object)
    log.info("Synchronisation des commandes terminée")
    log.info(f"{len(commands)} commandes synchronisées")

async def load():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            log.info(f"Extension {extension} chargée avec succès !")
        except Exception as e:
            log.info(f"Le chargement de l'extension {extension} a échoué...")
            log.error(e)


async def main():
    await init()
    await load()

    await bot.start(TOKEN)

asyncio.run(main())
