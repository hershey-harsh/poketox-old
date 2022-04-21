import sys
import traceback
import discord
from discord.ext import commands, tasks
import config

class Error_Hand(commands.Cog):
    """For basic bot operation."""

    def __init__(self, bot):
        self.bot = bot
   


    @commands.command()
    async def ping(self, ctx):
        """View the bot's latency."""

        message = await ctx.send("Pong!")
        seconds = (message.created_at - ctx.message.created_at).total_seconds()
        await message.edit(content=f"Pong! **{seconds * 1000:.0f} ms**")

def setup(bot):
    print("Loaded Error")
    bot.add_cog(Error_Hand(bot))
