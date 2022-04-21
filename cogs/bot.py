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

        if isinstance(error, commands.CommandOnCooldown):
            self.bot.log.info("Command cooldown hit", extra={"userid": ctx.author.id, "user": str(ctx.author)})
            await ctx.message.add_reaction("\N{HOURGLASS}")
        elif isinstance(error, commands.MaxConcurrencyReached):
            name = error.per.name
            suffix = "per %s" % name if error.per.name != "default" else "globally"
            plural = "%s times %s" if error.number > 1 else "%s time %s"
            fmt = plural % (error.number, suffix)
            await ctx.send(f"This command can only be used {fmt} at the same time.")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command cannot be used in private messages.")
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send("Sorry. This command is disabled and cannot be used.")
        elif isinstance(error, commands.BotMissingPermissions):
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
            return

    @commands.command()
    async def ping(self, ctx):
        """View the bot's latency."""

        message = await ctx.send("Pong!")
        seconds = (message.created_at - ctx.message.created_at).total_seconds()
        await message.edit(content=f"Pong! **{seconds * 1000:.0f} ms**")

def setup(bot):
    bot.add_cog(Error_Hand(bot))
