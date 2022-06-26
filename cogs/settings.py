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
    
    @commands.hybrid_group()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def setup(self, ctx):
        pass
    
    @setup.command(brief="Setup specialized pings")
    async def ping(self, ctx, select: Literal['Rare Pings', 'Alolan Pings', 'Galarian Pings', 'Hisuian Pings'], role: discord.Role = None):
            if role is None:
                return await ctx.send("Please select a role")
            
            if select == "Rare Pings":
                await self.bot.mongo.update_guild(
                    ctx.guild, {"$set": {"rareping": str(role.id)}}
                )
      
                embed=discord.Embed(title="Rare Pings", description=f"{role.mention} will be pinged when a Rare pokémon spawns", color=0x36393F)
                embed.set_thumbnail(url=ctx.guild.icon.url)
                await ctx.send(embed=embed)

            elif select == "Alolan Pings":
                await self.bot.mongo.update_guild(
                    ctx.guild, {"$set": {"alolanping": str(role.id)}}
                )
      
                embed=discord.Embed(title="Alolan Pings", description=f"{role.mention} will be pinged when a Alolan-Form pokémon spawns", color=0x36393F)
                embed.set_thumbnail(url=ctx.guild.icon.url)
                await ctx.send(embed=embed)

            elif select == "Galarian Pings":
                await self.bot.mongo.update_guild(
                    ctx.guild, {"$set": {"galarianping": str(role.id)}}
                )
      
                embed=discord.Embed(title="Galarian Pings", description=f"{role.mention} will be pinged when a Galarian-Form pokémon spawns", color=0x36393F)
                embed.set_thumbnail(url=ctx.guild.icon.url)
                await ctx.send(embed=embed)

            elif select == "Hisuian Pings":
                await self.bot.mongo.update_guild(
                    ctx.guild, {"$set": {"hisuianping": str(role.id)}}
                )
      
                embed=discord.Embed(title="Hisuian Pings", description=f"{role.mention} will be pinged when a Hisuian-Form pokémon spawns", color=0x36393F)
                embed.set_thumbnail(url=ctx.guild.icon.url)
                await ctx.send(embed=embed)
    
    @checks.has_started()
    @commands.has_permissions(manage_messages=True)
    @commands.hybrid_command(brief="Toggle server settings")
    async def raredex(self, ctx, role: Optional[discord.Role] = None):
            if role is None:
                return await ctx.send("Please use the Role option")
            else:
                await self.bot.mongo.update_guild(
                    ctx.guild, {"$set": {"rareping": str(role.id)}}
                )
      
                embed=discord.Embed(title="Raredex", description=f"{role.mention} will be pinged when a Rare pokémon spawns", color=0x36393F)
                embed.set_thumbnail(url=ctx.guild.icon.url)
                await ctx.send(embed=embed)
    
    
    @checks.has_started()
    @commands.has_permissions(manage_messages=True)
    @commands.hybrid_command(brief="Toggle server settings")
    async def toggle(self, ctx, select: Literal['Naming']):
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
            
        if select == "Starboard":
            if channel is None:
                return await ctx.send("Please use the Channel option")
            else:
                await self.bot.mongo.update_guild(
                    ctx.guild, {"$set": {"starboard": str(channel.id)}}
                )
      
                embed=discord.Embed(title="Starboard", description=f"All Rare pokémons will be sent to {channel.mention}", color=0x36393F)
                embed.set_thumbnail(url=ctx.guild.icon.url)
                await ctx.send(embed=embed)
        
    @checks.has_started()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.hybrid_command(brief="Disable your settings")
    async def disable(self, ctx, select: Literal['Pings', 'Catch Logs', 'Rare Dex'], serverid: Optional[str] = None, shinyhunt: Optional[Literal['Disable']] = None, collectlist: Optional[Literal['Disable']] = None):

        guildid = serverid
      
        if guildid == None:
          guildid = ctx.guild.id      
      
        if select == "Pings":
          if shinyhunt == "Disable":
                result = await self.bot.mongo.db.shinyhunt.update_one(
                    {"_id": ctx.author.id},
                    {"$unset": {str(ctx.guild.id): 1}},
                    upsert=True,
                )

                if result.upserted_id or result.modified_count > 0:
                    embed=discord.Embed(title="Shinyhunt Ping", description=f"You will not get pinged when your shiny hunt spawns in **{ctx.guild}**", color=0x36393F)
                    embed.set_thumbnail(url=ctx.guild.icon.url)
                    await ctx.send(embed=embed)
                else:
                    embed=discord.Embed(title="Shinyhunt Ping", description=f"This feature is already disabled in **{ctx.guild}**!", color=0x36393F)
                    embed.set_thumbnail(url=ctx.guild.icon.url)
                    return await ctx.send(embed=embed)
                
          if collectlist == "Disable":
                result = await self.bot.mongo.db.collector.update_one(
                    {"_id": ctx.author.id},
                    {"$unset": {str(ctx.guild.id): 1}},
                    upsert=True,
                )

                if result.upserted_id or result.modified_count > 0:
                    embed=discord.Embed(title="Collect List Ping", description=f"You will not get pinged when your collecting spawns in **{ctx.guild}**", color=0x36393F)
                    embed.set_thumbnail(url=ctx.guild.icon.url)
                    await ctx.send(embed=embed)
                else:
                    embed=discord.Embed(title="Collect List Ping", description=f"This feature is already disabled in **{ctx.guild}**!", color=0x36393F)
                    embed.set_thumbnail(url=ctx.guild.icon.url)
                    return await ctx.send(embed=embed)
          
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
            embed=discord.Embed(title="Ping", description=f"You will not get pinged when your shiny hunt and what your collecting spawns in **{ctx.guild}**", color=0x36393F)
            embed.set_thumbnail(url=ctx.guild.icon.url)
            await ctx.send(embed=embed)
          else:
            embed=discord.Embed(title="Ping", description=f"This feature is already disabled in **{ctx.guild}**!", color=0x36393F)
            embed.set_thumbnail(url=ctx.guild.icon.url)
            await ctx.send(embed=embed)
            
        if select == "Rare Dex":
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
    async def enable(self, ctx, select: Literal['Pings', 'Catch Logs', 'Rare Dex'], serverid: Optional[str] = None, shinyhunt: Optional[Literal['Enable']] = None, collectlist: Optional[Literal['Enable']] = None):

        guildid = serverid
      
        if guildid == None:
          guildid = ctx.guild.id      
      
        if select == "Pings":
            
          if shinyhunt == "Enable":
                result = await self.bot.mongo.db.shinyhunt.update_one(
                    {"_id": ctx.author.id},
                    {"$set": {str(ctx.guild.id): True}},
                    upsert=True,
                )

                if result.upserted_id or result.modified_count > 0:
                    embed=discord.Embed(title="Shinyhunt Ping", description=f"You will pinged when your shiny hunt spawns in **{ctx.guild}**", color=0x36393F)
                    embed.set_thumbnail(url=ctx.guild.icon.url)
                    return await ctx.send(embed=embed)
                else:
                    embed=discord.Embed(title="Shinyhunt Ping", description=f"This feature is already enabled in **{ctx.guild}**!", color=0x36393F)
                    embed.set_thumbnail(url=ctx.guild.icon.url)
                    return await ctx.send(embed=embed)
                
          if collectlist == "Enable":
                result = await self.bot.mongo.db.collector.update_one(
                    {"_id": ctx.author.id},
                    {"$set": {str(ctx.guild.id): True}},
                    upsert=True,
                )

                if result.upserted_id or result.modified_count > 0:
                    embed=discord.Embed(title="Collect List Ping", description=f"You will get pinged when your collecting spawns in **{ctx.guild}**", color=0x36393F)
                    embed.set_thumbnail(url=ctx.guild.icon.url)
                    return await ctx.send(embed=embed)
                else:
                    embed=discord.Embed(title="Collect List Ping", description=f"This feature is already enabled in **{ctx.guild}**!", color=0x36393F)
                    embed.set_thumbnail(url=ctx.guild.icon.url)
                    return await ctx.send(embed=embed)
          
          result = await self.bot.mongo.db.collector.update_one(
              {"_id": ctx.author.id},
              {"$set": {str(ctx.guild.id): True}},
              upsert=True,
          )
        
          result = await self.bot.mongo.db.shinyhunt.update_one(
              {"_id": ctx.author.id},
              {"$set": {str(ctx.guild.id): True}},
              upsert=True,
          )

          if result.upserted_id or result.modified_count > 0:
            embed=discord.Embed(title="Pings", description=f"You will get pinged when your shiny hunt spawns or what your collecting in **{ctx.guild}**", color=0x36393F)
            embed.set_thumbnail(url=ctx.guild.icon.url)
            await ctx.send(embed=embed)
          else:
            embed=discord.Embed(title="Pings", description=f"This feature is already enabled in **{ctx.guild}**!", color=0x36393F)
            embed.set_thumbnail(url=ctx.guild.icon.url)
            await ctx.send(embed=embed)
            
        if select == "Rare Dex":
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
                embed=discord.Embed(title="Rare dex", description=f"This feature is already enabled in **{ctx.guild}**!", color=0x36393F)
                embed.set_thumbnail(url=ctx.guild.icon.url)
                await ctx.send(embed=embed)            
            
        if select == "Catch Logs":
          
          result = await self.bot.mongo.db.catchlog.update_one(
              {"_id": ctx.author.id},
              {"$set": {str(ctx.guild.id): True}},
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
