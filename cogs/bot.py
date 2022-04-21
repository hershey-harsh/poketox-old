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
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            missing = [
                f"`{perm.replace('_', ' ').replace('guild', 'server').title()}`" for perm in error.missing_permissions
            ]
            fmt = "\n".join(missing)
            message = (
                f"💥 Err, I need the following permissions to run this command:\n{fmt}\nPlease fix this and try again."
            )
            botmember = self.bot.user if ctx.guild is None else ctx.guild.get_member(self.bot.user.id)
            if ctx.channel.permissions_for(botmember).send_messages:
                await ctx.send(message)

    @commands.Cog.listener()
    async def on_error(self, event, error):
        if isinstance(error, discord.NotFound):
            return
        else:
            print(f"Ignoring exception in event {event}:")
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command()
    async def ping(self, ctx):
        """View the bot's latency."""

        message = await ctx.send("Pong!")
        seconds = (message.created_at - ctx.message.created_at).total_seconds()
        await message.edit(content=f"Pong! **{seconds * 1000:.0f} ms**")

def setup(bot):
    print("Loaded Error")
    bot.add_cog(Error_Hand(bot))
