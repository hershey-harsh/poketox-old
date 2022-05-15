import discord
from discord.ext import commands
import random
import time
import math
from typing import Optional
import config

import asyncio
import requests
import json
import random
import asyncio
import datetime
from name import solve  
import discord
from data import models
from discord.ext import commands, menus
from helpers.converters import FetchUserConverter, SpeciesConverter
from helpers.pagination import AsyncListPageSource
from helpers import checks
import asyncio
from replit import db
import discord,random,os
import dbl
from discord.ext import commands
from typing import Literal

class comands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @checks.has_started()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.hybrid_command(brief="Disable Pings and Catch Logs")
    async def disable(self, ctx, select: Literal['Pings', 'Catch Logs'], ServerID: Optional[str] = None):

        guildid = ServerID
      
        if guildid == None:
          guildid = ctx.guild.id      
      
        if select == "Pings":
          
          result = await self.bot.mongo.db.collector.update_one(
              {"_id": ctx.author.id},
              {"$unset": {str(ctx.guild.id): 1}},
              upsert=True,
          )
        
          result = await self.bot.mongo.db.shinyhunt.update_one(
              {"_id": ctx.author.id},
              {"$unset": {str(ctx.guild.id): 1}},
              upsert=True,
          )

          if result.upserted_id or result.modified_count > 0:
            embed=discord.Embed(title="Ping", description=f"You will not get pinged when your shiny hunt or what your collecting spawns in **{ctx.guild}**", color=0x36393F)
            embed.set_thumbnail(url=ctx.guild.icon.url)
            await ctx.send(embed=embed)
          else:
            embed=discord.Embed(title="Ping", description=f"This feature is already disabled in **{ctx.guild}**!", color=0x36393F)
            embed.set_thumbnail(url=ctx.guild.icon.url)
            await ctx.send(embed=embed)
            
        if select == "Catch Log":
          
          result = await self.bot.mongo.db.catchlog.update_one(
              {"_id": ctx.author.id},
              {"$unset": {str(ctx.guild.id): 1}},
              upsert=True,
          )

          if result.upserted_id or result.modified_count > 0:
            embed=discord.Embed(title="Catch Log", description=f"Your spawns will not be tracked in in **{ctx.guild}**", color=0x36393F)
            embed.set_thumbnail(url=ctx.guild.icon.url)
            await ctx.send(embed=embed)
          else:
            embed=discord.Embed(title="Ping", description=f"This feature is already disabled in **{ctx.guild}**!", color=0x36393F)
            embed.set_thumbnail(url=ctx.guild.icon.url)
            await ctx.send(embed=embed)
        
async def setup(bot):
    print("Loaded Catch Logger")
    await bot.add_cog(comands(bot))
