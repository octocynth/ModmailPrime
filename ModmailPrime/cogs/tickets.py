from discord.ext.commands import Cog


class Tickets(Cog):
    pass


def setup(bot):
    bot.add_cog(Tickets(bot))
