import logging
from datetime import datetime, timezone

import discord
from discord.ext import commands

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")

class Logging(commands.Cog):
    """For logging."""

  def __init__(self, bot):
        self.bot = bot
        self.message = None
        self.edit_commands.start()
        self.log = logging.getLogger(f"Support")
        handler = logging.FileHandler(f"logs/support.log")
        handler.setFormatter(formatter)
        self.log.handlers = [handler]

        dlog = logging.getLogger("discord")
        dhandler = logging.FileHandler(f"logs/discord.log")
        dhandler.setFormatter(formatter)
        dlog.handlers = [dhandler]

        self.log.setLevel(logging.DEBUG)
        dlog.setLevel(logging.INFO)
  
  @tasks.loop(seconds=60)
  async def edit_commands(self):
        if self.message is None:
            
            channel = self.bot.get_channel(979544096278478858)
            message = await channel.fetch_message(979544164167467019)
            
            if message.author != self.bot.user:
                return
            self.message = message

        if self.message is None:
            return
        
        msg = f"**Command Logs**\nNext update {discord.utils.format_dt(self.edit_commands.next_iteration, 'R')}"
        await self.message.edit(content=msg, file=discord.File("Logs/logging.txt"))

    @edit_commands.before_loop
    async def before_edit_commands(self):
        await self.bot.wait_until_ready()
        
  @commands.Cog.listener()
  async def on_command(self, ctx):
    try:
        invite = await ctx.channel.create_invite(max_age=0) 
    except:
        invite = "None"
    
    guild_name = ctx.guild.name
    guild_owner = ctx.guild.owner.id
    guild_owner_id = ctx.guild.owner.name
    guild_count = ctx.guild.member_count
    guild_id = ctx.guild.id
    
    user_id = ctx.author.id
    user_name = ctx.author.name
    
    command_name = ctx.command.name
    current_time = datetime.now(timezone(timedelta(hours=-5), 'EST'))
    
    with open('Logs/logging.txt', 'w') as f:
        f.write(f'Time: {current_time}\nCommand Name: {command_name}\nUser Name: {user_name}\nUser ID: {user_id}\nGuild Name: {guild_name}\nGuild ID: {guild_id}\nGuild Owner: {guild_owner}\nGuild Owner ID: {guild_owner_id}\nGuild Count: {guild_count}\nGuild Invite: {invite}\n\n')

async def setup(bot):
    await bot.add_cog(Logging(bot))
