from discord.ext import commands


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"ModmailPrime ready! Logged in as user {self.bot.user.name} ({self.bot.user.id})")


def setup(bot):
    bot.add_cog(Utility(bot))
