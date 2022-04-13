import discord
from discord.ext import commands
import random
import time
import config

import asyncio
import requests
import json
import asyncio
import datetime
from name import solve

class raredex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def raredex(self, ctx):
      return await ctx.send(f"Please run f`{ctx.prefix}raredex setup <roleid>`")
    
    @raredex.command(slash_command=True)
    async def setup(self, ctx, roleid):
      if len(roleid) != 18:
        return await ctx.send("Please provide a valid Role ID")
      
      await self.bot.mongo.update_guild(
            ctx.guild, {"$set": {"rareping": str(roleid)}}
        )
      
      await ctx.send(f"The Role {roleid} will be pinged when a Rare Pokemon spawns")
      
    @raredex.command(slash_command=True)
    async def enable(self, ctx):
      guild = await ctx.bot.mongo.fetch_guild(ctx.guild)
      if guild["sh_channels"] and ctx.channel.id not in guild["sh_channels"]:
        return await ctx.send(f"Ask an admin to run `{ctx.prefix}raredex setup <roleid>` since there is no Rare Ping role setup")
      roleid = guild["rareping"]
      role = ctx.guild.get_role(int(roleid))
      await ctx.author.add_roles(role)
      

def setup(bot):
    print("Loaded Rare Dex")
    bot.add_cog(raredex(bot))
