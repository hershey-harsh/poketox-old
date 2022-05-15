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
import discord
from discord.ext import commands, menus
from helpers.converters import FetchUserConverter, SpeciesConverter
from helpers.pagination import AsyncListPageSource
from helpers import checks
import asyncio
from replit import db
import discord,random,os
from discord.ext import commands


class raredex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
   
    @checks.has_started()
    @commands.group(invoke_without_command=True)
    async def raredex(self, ctx):
      embed=discord.Embed(title="Rare Dex", color=0x36393F)
      embed.add_field(name="Setup | Setup Rare Dex in your server", value=f"```\n{ctx.prefix}raredex setup <roleid>```", inline=False)
      embed.add_field(name="Enable | Enables pings for Rare Dex", value=f"```diff\n+ {ctx.prefix}!raredex enable```", inline=False)
      embed.add_field(name="Disable | Disable pings for Rare Dex", value=f"```diff\n- {ctx.prefix}raredex disable```")
      await ctx.send(embed=embed)
    
    @checks.has_started()
    @commands.has_permissions(manage_messages=True)
    @raredex.command()
    async def setup(self, ctx, roleid):
      if len(roleid) != 18:
        return await ctx.send("Please provide a valid Role ID")
      
      await self.bot.mongo.update_guild(
            ctx.guild, {"$set": {"rareping": str(roleid)}}
        )
      
      await ctx.send(f"The Role {roleid} will be pinged when a Rare Pokemon spawns")

async def setup(bot):
    print("Loaded Rare Dex")
    await bot.add_cog(raredex(bot))
