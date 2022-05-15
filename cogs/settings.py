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

class catch_log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @checks.has_started()           
    @commands.hybrid_command(brief="Toggle server settings")
    async def toggle(self, ctx, select: Literal['Naming', 'Raredex Setup'], role: Optional[discord.Role] = None):
        if select == "Raredex Setup":
            if role is None:
                return await ctx.send("Please use the Role option")
            else:
                await self.bot.mongo.update_guild(
                    ctx.guild, {"$set": {"rareping": str(role.id)}}
                )
      
                embed=discord.Embed(title="Raredex", description=f"{role.mention} will be pinged when a Rare pokémon spawns", color=0x36393F)
                embed.set_thumbnail(url=ctx.guild.icon.url)
                await ctx.send(embed=embed)
            
        if select == "Naming":
            guild = await ctx.bot.mongo.fetch_guild(ctx.guild)
            
            mode = guild["name"]
            
            if mode == "On":
                mode = "Off"
            
            elif mode == "Off":
                mode = "On"
            
            else:
                mode = "Off"
      
            await self.bot.mongo.update_guild(
                ctx.guild, {"$set": {"name": str(mode)}}
            )
        
            embed=discord.Embed(title="Spawn Naming", description=f"Toggled spawn naming to {mode}", color=0x36393F)
            embed.set_thumbnail(url=ctx.guild.icon.url)
            await ctx.send(embed=embed)
        
    @checks.has_started()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.hybrid_command(brief="Disable your settings")
    async def disable(self, ctx, select: Literal['Pings', 'Raredex', 'Catch Logs'], serverid: Optional[str] = None):

        guildid = serverid
      
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
            
        if select == "Raredex":
            guild = await ctx.bot.mongo.fetch_guild(ctx.guild)
            try:
                roleid = guild["rareping"]
            except:
                roleid = None

         
            if roleid == None:
                return await ctx.send(f"Ask an admin to run `{ctx.prefix}raredex setup <roleid>` since there is no Rare Ping role setup")
      
            roleid = guild["rareping"]
            role = ctx.guild.get_role(int(roleid))
            try:
                await ctx.author.remove_roles(role)  
                embed=discord.Embed(title="Rare Dex", description="You will not get pinged when a Rare Pokemon spawns", color=0x36393F)
                await ctx.send(embed=embed)
            except:
                embed=discord.Embed(title="Raredex", description=f"This feature is already disabled in **{ctx.guild}**!", color=0x36393F)
                embed.set_thumbnail(url=ctx.guild.icon.url)
                await ctx.send(embed=embed)
            
        if select == "Catch Logs":
          
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
            
    @checks.has_started()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.hybrid_command(brief="Enable your settings")
    async def enable(self, ctx, select: Literal['Pings', 'Catch Logs'], serverid: Optional[str] = None):

        guildid = serverid
      
        if guildid == None:
          guildid = ctx.guild.id      
      
        if select == "Pings":
          
          result = await self.bot.mongo.db.collector.update_one(
              {"_id": ctx.author.id},
              {"$unset": {str(ctx.guild.id): True}},
              upsert=True,
          )
        
          result = await self.bot.mongo.db.shinyhunt.update_one(
              {"_id": ctx.author.id},
              {"$unset": {str(ctx.guild.id): True}},
              upsert=True,
          )

          if result.upserted_id or result.modified_count > 0:
            embed=discord.Embed(title="Catch Logs", description=f"You will get pinged when your shiny hunt spawns or what your collecting in **{ctx.guild}**", color=0x36393F)
            embed.set_thumbnail(url=ctx.guild.icon.url)
            await ctx.send(embed=embed)
          else:
            embed=discord.Embed(title="Catch Logs", description=f"This feature is already enabled in **{ctx.guild}**!", color=0x36393F)
            embed.set_thumbnail(url=ctx.guild.icon.url)
            await ctx.send(embed=embed)
            
        if select == "Raredex":
            guild = await ctx.bot.mongo.fetch_guild(ctx.guild)
            try:
                roleid = guild["rareping"]
            except:
                roleid = None

         
            if roleid == None:
                return await ctx.send(f"Ask an admin to run `{ctx.prefix}raredex setup <roleid>` since there is no Rare Ping role setup")
      
            roleid = guild["rareping"]
            role = ctx.guild.get_role(int(roleid))
            try:
                await ctx.author.add_roles(role)  
                embed=discord.Embed(title="Rare Dex", description="You **will** now get pinged whenever a Rare Pokemon spawns", color=0x36393F)
                await ctx.send(embed=embed)
            except:
                embed=discord.Embed(title="Raredex", description=f"This feature is already enabled in **{ctx.guild}**!", color=0x36393F)
                embed.set_thumbnail(url=ctx.guild.icon.url)
                await ctx.send(embed=embed)            
            
        if select == "Catch Logs":
          
          result = await self.bot.mongo.db.catchlog.update_one(
              {"_id": ctx.author.id},
              {"$unset": {str(ctx.guild.id): 1}},
              upsert=True,
          )

          if result.upserted_id or result.modified_count > 0:
            embed=discord.Embed(title="Catch Logs", description=f"Your spawns will be tracked in in **{ctx.guild}**", color=0x36393F)
            embed.set_thumbnail(url=ctx.guild.icon.url)
            await ctx.send(embed=embed)
          else:
            embed=discord.Embed(title="Catch Logs", description=f"This feature is already enabled in **{ctx.guild}**!", color=0x36393F)
            embed.set_thumbnail(url=ctx.guild.icon.url)
            await ctx.send(embed=embed)
        
async def setup(bot):
    print("Loaded Catch Logger")
    await bot.add_cog(catch_log(bot))