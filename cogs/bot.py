import sys
import traceback
import discord
from discord.ext import commands, tasks
import copy
import config

GENERAL_CHANNEL_NAMES = {"welcome", "general", "lounge", "chat", "talk", "main", ""}

class But(discord.ui.View):
    def __init__(self, query=None):
        super().__init__()
        if query is not None:
            self.add_item(discord.ui.Button(label='Command Usage', url=query))
        self.add_item(discord.ui.Button(label='Community Server', url="https://discord.gg/XmbRtpr4"))

class Error_Hand(commands.Cog):
    """For basic bot operation."""

    def __init__(self, bot):
        self.bot = bot
        self.message = None
        self.edit_status.start()
        
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        priority_channels = []
        channels = []
        for channel in guild.channels:
            if channel == guild.system_channel or any(x in channel.name for x in GENERAL_CHANNEL_NAMES):
                priority_channels.append(channel)
            else:
                channels.append(channel)
        channels = priority_channels + channels
        try:
            channel = next(
                x for x in channels if isinstance(x, TextChannel) and x.permissions_for(guild.me).send_messages
            )
        except StopIteration:
            return
        prefix = "a!"

        embed = self.bot.Embed(
            title="Pokétox",
            description=f"To get setup pokétox, firstly do `{prefix}help Whitelist` to learn how to whitelist pinging channels. If you want to get pinged for your Shinyhunt/Collectlist then please do `{prefix}enable Pings`! Do `{prefix}help collectlist` or `{prefix}help shinyhunt`! For a full command list, do `{prefix}help`.",
            color=0x2F3136
        )

        embed.add_field(
            name="Support Server",
            value="Join our server at [discord.gg/poketox](https://discord.gg/YmVA2ah5tE) for support.",
            inline=False,
        )
        await channel.send(embed=embed)
        
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.content != before.content:
            after.content = after.content.replace("—", "--").replace("'", "′").replace("‘", "′").replace("’", "′")
            await self.bot.process_commands(after)
   
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        
        if isinstance(error, commands.NoPrivateMessage):
            
            full = ctx.command.full_parent_name
            if ctx.command.name is not None:
                full = full+" "+ctx.command.name
            
            embed=discord.Embed(title="Command Unusable", description=f"{full.title()} is unusable in private messages. Try running {full.title()} in a server.", color=0x2F3136)
            await ctx.send(embed=embed, view=But())
            
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.message.add_reaction("\N{HOURGLASS}")
            
        elif isinstance(error, commands.DisabledCommand):
            embed=discord.Embed(title="Command Disabled", description=f"{full.title()} is disabled. Check <#968961636826243112> in the Community Server for updates.", color=0x2F3136)
            await ctx.send(embed=embed, view=But())
            
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
            commands_link = {

                "shinyhunt view" : "https://docs.poketox.me/shiny-hunt-pings/shiny-hunt-view",
                "shinyhunt set" : "https://docs.poketox.me/shiny-hunt-pings/shiny-hunt-set",
                "shinyhunt clear" : "https://docs.poketox.me/shiny-hunt-pings/shiny-hunt-clear",
                "shinyhunt search" : "https://docs.poketox.me/shiny-hunt-pings/shiny-hunt-search",
                "shinyhunt globalsearch" : "https://docs.poketox.me/shiny-hunt-pings/shiny-hunt-globalsearch",
                "collectlist view" : "https://docs.poketox.me/collectlist-pings/collectlist-view",
                "collectlist add" : "https://docs.poketox.me/collectlist-pings/collectlist-add",
                "collectlist multiadd" : "https://docs.poketox.me/collectlist-pings/collectlist-multi-add",
                "collectlist multiremove" : "https://docs.poketox.me/collectlist-pings/collectlist-multi-remove",
                "collectlist remove" : "https://docs.poketox.me/collectlist-pings/collectlist-remove",
                "collectlist clear" : "https://docs.poketox.me/collectlist-pings/collectlist-clear",
                "collectlist search" : "https://docs.poketox.me/collectlist-pings/collectlist-search",
                "collectlist globalsearch" : "https://docs.poketox.me/collectlist-pings/collectlist-globalsearch",
            }
            
            commands_usage = {
                
                "shinyhunt view" : "a!shinyhunt view",
                "shinyhunt set" : "a!shinyhunt set <pokémon>",
                "shinyhunt clear" : "a!shinyhunt clear",
                "shinyhunt search" : "a!shinyhunt search <pokémon>",
                "shinyhunt globalsearch" : "a!shinyhunt globalsearch <pokémon>",
                "collectlist view" : "a!collectlist view",
                "collectlist add" : "a!collectlist add <pokémon>",
                "collectlist multiadd" : "a!collectlist multiadd <pokémon1>, <pokémon2>, <pokémon3>",
                "collectlist multiremove" : "a!collectlist multiremove <pokémon1>, <pokémon2>, <pokémon3>",
                "collectlist remove" : "a!collectlist remove <pokémon>",
                "collectlist clear" : "a!collectlist clear",
                "collectlist search" : "a!collectlist search <pokémon>",
                "collectlist globalsearch" : "a!collectlist globalsearch <pokémon>",
            }
            
            try:
                full = ctx.command.full_parent_name
                
                if ctx.command.name is not None:
                    full = full+" "+ctx.command.name
                    
                command_usg = commands_usage[full]
                embed=discord.Embed(title="Command Error", description=f"Click the command or the button below to read more \ndocumentation on {full}\n[```{command_usg}```]({commands_link[full]})", color=0x2F3136)
                await ctx.send(embed=embed, view=But(commands_link[full]))
            except Exception as e:
                print(e)
            
        elif isinstance(error, commands.ConversionError):
            await ctx.send(error.original)
            
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
        
        total_members = total_members + 200000
        total_members = "{:,}".format(int(total_members))
            
        registered = await self.bot.mongo.db.member.estimated_document_count()
        total_registred = registered + 200000
        total_registred = "{:,}".format(int(total_registred))
        
        msg = f"**Live Status**\nNext update {discord.utils.format_dt(self.edit_status.next_iteration, 'R')}\n\nPing: {round (self.bot.latency * 1000)}ms\nServers: {len(self.bot.guilds)}\nMembers: {total_members}\nRegistered Users: {total_registred}"
        
        await self.message.edit(content=msg)
        
    @edit_status.before_loop
    async def before_edit_status(self):
        await self.bot.wait_until_ready()
        
async def setup(bot):
    print("Loaded Error")
    await bot.add_cog(Error_Hand(bot))
