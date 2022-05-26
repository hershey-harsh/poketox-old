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
        self.message = None
        self.edit_status.start()
        
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
            await ctx.message.add_reaction("\N{HOURGLASS}")
            
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
            
        elif isinstance(error, commands.ConversionError):
            await ctx.send(error.original)
                
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send_help(ctx.command)
            
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

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def cleanup(self, ctx, search=100):
        """Cleans up the bot's messages from the channel."""

        def check(m):
            return m.author == ctx.me or m.content.startswith(ctx.prefix)

        deleted = await ctx.channel.purge(limit=search, check=check, before=ctx.message)
        spammers = Counter(m.author.display_name for m in deleted)
        count = len(deleted)

        messages = [f'{count} message{" was" if count == 1 else "s were"} removed.']
        if len(deleted) > 0:
            messages.append("")
            spammers = sorted(spammers.items(), key=lambda t: t[1], reverse=True)
            messages.extend(f"– **{author}**: {count}" for author, count in spammers)

        await ctx.send("\n".join(messages), delete_after=5)
        
    @tasks.loop(seconds=30)
    async def edit_status(self):
        if self.message is None:
            
            channel = self.bot.get_channel(979173373991067658)
            message = await channel.fetch_message(979176488022704240)
            
            if message.author != self.bot.user:
                return
            self.message = message

        if self.message is None:
            return
        
        total_members = 0
        for guild in self.bot.guilds:
            total_members += guild.member_count
            total_members = "{:,}".format(int(total_members))
            
        registered = await self.bot.mongo.db.member.estimated_document_count()
        total_registred = registered + 200000
        total_registred = "{:,}".format(int(total_registred))
        
        msg = f"""
        **Live Status**\nNext update {discord.utils.format_dt(self.edit_status.next_iteration, 'R')}\n\nPing: {round (self.bot.latency * 1000)}ms\nServers: {len(self.bot.guilds)}\nMembers: {total_members + 200000}\nRegistered Users: {total_registred}
        """
        
        await self.message.edit(content=msg)
        
    @edit_status.before_loop
    async def before_edit_status(self):
        await self.bot.wait_until_ready()
        
async def setup(bot):
    print("Loaded Error")
    await bot.add_cog(Error_Hand(bot))
