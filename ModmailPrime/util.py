from enum import Enum, auto

from discord.ext.commands import NotOwner, check


def is_dev():
    def cog_check(ctx):
        if ctx.author.id not in ctx.bot.bot_config['developers']:
            raise NotOwner('you are not a developer!')
        return True
    return check(cog_check)


class StatusAction(Enum):
    OPEN = auto()
    CLOSED = auto()
    STALLED = auto()

