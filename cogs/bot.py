import sys
import traceback
import discord
from discord.ext import commands, tasks
import copy
import config

class Error_Hand(commands.Cog):
    """For basic bot operation."""

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.content != before.content:
            after.content = after.content.replace("—", "--").replace("'", "′").replace("‘", "′").replace("’", "′")
            await self.bot.process_commands(after)
   
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command cannot be used in private messages.")
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title=f"Slow it down!",
                description=f"Try again in {int(float(error.retry_after:.2f))} seconds",
                color=0x99A7F9
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send("Sorry. This command is disabled and cannot be used.")
        elif isinstance(error, commands.BotMissingPermissions):
            missing = [
                "> **" + perm.replace("_", " ").replace("guild", "server").title() + "**"
                for perm in error.missing_permissions
            ]
            fmt = "\n".join(missing)
            message = f"Something went wrong! I am missing the following permissions to run this command:\n\n{fmt}\n\n Please fix this and try again."
            try:
                await ctx.send(message)
            except:
                pass
                
        elif isinstance(error, commands.MissingRequiredArgument):
            con = copy.copy(ctx)
            con.content = f'{ctx.prefix}help {ctx.command}'
            
            await self.bot.process_commands(con)
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(error)
        elif isinstance(error, commands.UserInputError):
            await ctx.send(error)
        elif isinstance(error, commands.CommandNotFound):
            return
        else:
            print(f"Ignoring exception in command {ctx.command}")
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr
            )

    @commands.Cog.listener()
    async def on_error(self, event, error):
        if isinstance(error, discord.NotFound):
            return
        else:
            print(f"Ignoring exception in event {event}:")
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr
            )

    @commands.command()
    async def ping(self, ctx):
        """View the bot's latency."""

        message = await ctx.send("Pong!")
        seconds = (message.created_at - ctx.message.created_at).total_seconds()
        await message.edit(content=f"Pong! **{seconds * 1000:.0f} ms**")

def setup(bot):
    print("Loaded Error")
    bot.add_cog(Error_Hand(bot))
