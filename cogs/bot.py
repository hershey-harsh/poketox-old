import sys
import traceback
import discord
from discord.ext import commands, tasks
import config

class Error_Hand(commands.Cog):
    """For basic bot operation."""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):

        # raise error
        # Command not found
        if isinstance(error, commands.CommandNotFound):
            await ctx.message.add_reaction("⁉️")
            message = "Command not found."
        # On cooldown
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.message.add_reaction("❌")
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
        # User doesn't have permissions
        elif isinstance(error, commands.MissingPermissions):
            await ctx.message.add_reaction("🔐")
            message = "No permissions."
        elif isinstance(error, commands.BadArgument):
            await ctx.message.add_reaction("🤏")
            message = "Bad arguement."
        # Not enough args
        elif isinstance(error, commands.UserInputError):
            await ctx.message.add_reaction("🤏")
            message = f"Not all required arguements were passed, do `{prefix}!help {ctx.message.content[2:]}`"
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.add_reaction("🤏")
            message = f"Not all required arguements were passed, do `{prefix}!help {ctx.message.content[2:]}`"
        # Mentioned member not found
        elif isinstance(error, commands.MemberNotFound):
            await ctx.message.add_reaction("🤷‍♂️")
            message = "Couldn't find that member."
        # Bot doesn't have permissions
        elif isinstance(error.original, discord.errors.Forbidden):
            message = "Bot doesn't have the permissions needed."
            await ctx.send(message)
        else:
            message = "This is an undocumented error, it has been reported and will be patched in the next update."
            raise error

    @commands.command()
    async def ping(self, ctx):
        """View the bot's latency."""

        message = await ctx.send("Pong!")
        seconds = (message.created_at - ctx.message.created_at).total_seconds()
        await message.edit(content=f"Pong! **{seconds * 1000:.0f} ms**")

def setup(bot):
    print("Loaded Error")
    bot.add_cog(Error_Hand(bot))
