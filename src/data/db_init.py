from tortoise import Tortoise, run_async
from data.models import *

import logging
log = logging.getLogger("LeGuMe")

configuration = {
    'connections': {
        'default': 'sqlite://data/db.sqlite3',
    },
    'apps': {
        'models': {
            'models': ['data.models']
        }
    }
}

async def init():
    await Tortoise.init(
        config = configuration
    )
    await Tortoise.generate_schemas()

    CATEGORIES = (
        "Binary Exploitation",
        "Cryptography",
        "Forensics",
        "Reverse",
        "Web",
    )

    categories = await Category.all()
    if len(categories) == 0:
        for category in CATEGORIES:
            await Category.create(name = category.lower())


if __name__ == "__main__":
    run_async(init())
