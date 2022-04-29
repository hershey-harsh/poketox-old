from discord.ext import commands

from data import DataManager


class Data(commands.Cog):
    """For game data."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.instance = DataManager()


async def setup(bot):
    await bot.add_cog(Data(bot))
