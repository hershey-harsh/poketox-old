import discord
from discord.ext import commands
import random
import time
import math
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
import dbl
from discord.ext import commands

class comands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dblpy = dbl.DBLClient(self.bot, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijg3NTUyNjg5OTM4Njk1Mzc3OSIsImJvdCI6dHJ1ZSwiaWF0IjoxNjUwNDE0MjMzfQ.7aZSEjaVH-lH-KtBe_Q2pmGA-wnbyLLbODxEhcfghAE")
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.embeds and message.channel.id == 966129589275471902:
            voter_id = message.embeds[0].footer.value
            
    @checks.has_started()
    @commands.command(brief="Suggest new features")
    async def suggest(self, ctx, *, args):
      chan = self.bot.get_channel(939162941536735292)
      
      embed=discord.Embed(title="💡 Suggestion", color=0x5865F2)
      embed.add_field(name="Server", value=f"{ctx.guild} (*{ctx.guild.id}*)", inline=True)
      embed.add_field(name="User", value=f"{ctx.author.mention} (*{ctx.author.id}*)", inline=True)
      embed.add_field(name="Suggestion", value=f'> "{args}"', inline=False)
      
      await chan.send(embed=embed) 
        
      embed=discord.Embed(title="Suggestion Sent", color=0x2F3136)
        
    @checks.has_started()
    @commands.is_owner()
    @commands.command()
    async def dm(ctx, user: discord.User, *, message=None):
        await user.send(message)
        await ctx.send("Sent Message")
          
    @checks.has_started()
    @commands.command()
    async def botstats(self, ctx):
        """Pokétox stats"""

        embed = discord.Embed(color=0x2F3136, title = f"Pokétox Statistics")
        embed.add_field(
            name = "Total servers", 
            value = f"{len(self.bot.guilds)}", 
            inline = False
        )

        total_members = 0
        for guild in self.bot.guilds:
            total_members += guild.member_count

        embed.add_field(
            name = "Total Members", 
            value = f"{total_members}",
            inline = False
        )

        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/875526899386953779/d46976087eef1662db19c8272ebb57e4.png?size=1024")
        await ctx.send(embed = embed)
        
    @checks.has_started()
    @commands.command()
    async def vote(self, ctx):
        """Vote for the Pokétox"""

        embed = discord.Embed(color=0x2F3136, title = f"Vote for the bot below")
        embed.add_field(
            name = "Vote for the bot", 
            value = f"[Top.gg bot voting](https://top.gg/bot/875526899386953779/vote)", 
            inline = False
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/875526899386953779/d46976087eef1662db19c8272ebb57e4.png?size=1024")
        await ctx.send(embed=embed)
        
    @checks.has_started()
    @commands.command(aliases=("sr",))
    async def shinyrate(self, ctx, streak=1):
        """Check the shinyrate for a specific shiny hunt streak"""
        
        wsc = f'{4096/(1+math.log(1+streak/30)): .3f}'
        wsc = "{:,}".format(int(float(wsc)))

        embed = discord.Embed(color=0x2F3136, title = f"Shiny Rate", description=f"Shiny Rate for {streak} shiny hunt streak")
        embed.add_field(
            name = "Without shiny charm", 
            value = f"1 in {wsc}", 
            inline = False
        )
        
        wsc = f'{3413.33/(1+math.log(1+streak/30)): .3f}'
        wsc = "{:,}".format(int(float(wsc)))
        
        embed.add_field(
            name = "With shiny charm", 
            value = f"1 in {wsc}",
            inline = False
        )
        await ctx.send(embed = embed)
      
def setup(bot):
    print("Loaded Commands")
    bot.add_cog(comands(bot))
