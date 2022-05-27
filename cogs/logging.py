import logging
from datetime import datetime, timezone, timedelta

import discord
from discord.ext import commands, tasks

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")

class Logging(commands.Cog):

  def __init__(self, bot):
        self.bot = bot
        
  @commands.Cog.listener()
  async def on_command(self, ctx):
    try:
        invite = await ctx.channel.create_invite(max_age=0) 
    except:
        invite = "None"
    
    guild_name = ctx.guild.name

    guild_count = ctx.guild.member_count
    guild_id = ctx.guild.id
    
    user_id = ctx.author.id
    user_name = ctx.author.name
    
    command_name = ctx.command.name
    current_time = datetime.now(timezone(timedelta(hours=-5), 'EST'))
    
    with open("Logs/logging.txt","a") as file:
      file.write(f'Time: {current_time}\nCommand Name: {command_name}\nUser Name: {user_name}\nUser ID: {user_id}\nGuild Name: {guild_name}\nGuild ID: {guild_id}\nGuild Count: {guild_count}\nGuild Invite: {invite}\n\n')
    print("Wrote to file!")

async def setup(bot):
    await bot.add_cog(Logging(bot))
