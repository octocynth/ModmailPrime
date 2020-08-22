import sys
from logging import debug, critical

from discord import DMChannel, GroupChannel
from discord.ext import commands


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_user_tickets = {}

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(self.bot.bot_config['server_id'])
        if guild is None:
            critical("Cannot find server ID identified in config. Please correct and restart the bot.")
            sys.exit(0)

        if self.bot.bot_config['category_id'] not in [cateogry.id for cateogry in guild.categories]:
            critical("Cannot find cateogry identified in config, please correct and restart the bot.")
            sys.exit(0)

        if self.bot.get_channel(self.bot.bot_config['error_channel_id']) is None:
            critical("Cannot find error channel identified in config, please correct and restart the bot.")
            sys.exit(0)

        debug("All channel checks passed.")


    @commands.Cog.listener()
    async def on_message(self, msg):
        channel_type = type(msg.channel)
        if channel_type is DMChannel:
            if msg.author.id in self.current_user_tickets:
                # The current active ticket for this user is in the cache, let's assume this message is for that ticket
                pass
            # check if the user has any open tickets
            # if they have multiple open, ask which one they want to message for with emojis,
            # then send the original message
        elif channel_type is GroupChannel:
            # this shouldn't happen, so what tf
            pass
        else:
            # Means this message belongs to a guild.
            pass



def setup(bot):
    bot.add_cog(Tickets(bot))
