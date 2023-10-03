from tortoise.models import Model
from tortoise import fields
from datetime import date

import logging
log = logging.getLogger("LeGuMe")

class Course(Model):
    """
    Represents a HDFR Course, contains a list of challenges
    """
    id         = fields.UUIDField(pk = True)
    name       = fields.CharField(max_length = 255)
    challenges = fields.ManyToManyField("models.Challenge", "courses")
    active     = fields.BooleanField()

class Category(Model):
    """
    Represents a Challenge Category, for instance "Cryptography"
    """
    name = fields.CharField(max_length = 255, pk = True)

class Challenge(Model):
    """
    Represents a HDFR Challenge.
    """
    id       = fields.UUIDField(pk = True)
    category = fields.ForeignKeyField("models.Category", "challenges")
    name     = fields.CharField(max_length = 255)
    points   = fields.IntField()
    desc     = fields.CharField(max_length = 4000)
    flag     = fields.CharField(max_length = 255)

    def __str__(self):
        return f"[{self.category.name}/{self.name} ({self.points})]"

class Flag(Model):
    """
    Represents a user resolution of a challenge.
    """
    id        = fields.UUIDField(pk=True)
    challenge = fields.ForeignKeyField("models.Challenge", "solves")
    user      = fields.ForeignKeyField("models.User", "solved_challenges", null=True, default=None)
    date      = fields.DateField()


class User(Model):
    """
    Represents a HDFR member.
    """
    id          = fields.BigIntField(pk=True)
    server_rank = fields.IntField(default=2147483647)

    async def score(self) -> int:
        result = 0
        solved_challenges = await self.solved_challenges.all().prefetch_related("challenge")
        for flag in solved_challenges:
            result += flag.challenge.points
        return result

    async def add_flag(self, challenge: Challenge) -> None:
        await Flag.create(date=date.today(), challenge=challenge, user=self)

    @classmethod
    async def from_discord_user(cls, user) -> bool:
        existing_user = await cls.filter(id=user.id).first()
        if existing_user is None:
            user = await cls.create(id=user.id)
            return user
        return existing_user

    def __str__(self) -> str:
        return f"{self.id} (#{self.server_rank})"
