from discord.ext import commands
import discord
import logging


class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        logging.getLogger().addHandler(DiscordLogger(self.bot))

    @commands.Cog.listener()
    async def on_disconnect(self):
        logging.getLogger().removeHandler(DiscordLogger)


def setup(bot):
    bot.add_cog(Log(bot))


class DiscordLogger(logging.StreamHandler):
    """
    A handler class which sends messages to a Discord channel
    """
    LEVEL_COLORS = {
        logging.NOTSET: discord.colour.Color.darker_grey(),
        logging.DEBUG: discord.colour.Color.blue(),
        logging.INFO: discord.colour.Color.green(),
        logging.WARNING: discord.colour.Color.gold(),
        logging.ERROR: discord.colour.Color.red(),
        logging.CRITICAL: discord.colour.Color.red(),
    }

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.setLevel(logging.WARN)

    def emit(self, record):
        self.bot.loop.create_task(self.send_discord_err(record))

    async def send_discord_err(self, record):
        channel = self.bot.get_channel(self.bot.bot_config['error_channel_id'])
        embed = discord.Embed(title=f"{record.levelname} in {record.name}")
        embed.description = f"```{record.getMessage()}```"
        embed.colour = self.LEVEL_COLORS[record.levelno]
        if record.exc_text is not None:
            embed.add_field(name="Exception Info", value=record.exc_text)
        embed.add_field(name=f"Error in {record.funcName} on line {record.lineno}", value=record.filename)
        try:
            await channel.send(embed=embed)
        except (RuntimeError, discord.ClientException):
            # RuntimeError: raised by aiohttp when the bot is closing; quiets log spam on exit
            # ClientException: raised when we can't send the message; prevents infinite cycle of errors
            pass
