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

class comands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
   
    @commands.command(brief="Suggest new features")
    async def suggest(self, ctx, *, args):
      chan = self.bot.get_channel(939162941536735292)
      
      embed=discord.Embed(title="💡 Suggestion", color=0x5865F2)
      embed.add_field(name="Server", value=f"{ctx.guild} (*{ctx.guild.id}*)", inline=True)
      embed.add_field(name="User", value=f"{ctx.author.mention} (*{ctx.author.id}*)", inline=True)
      embed.add_field(name="Suggestion", value=f'> "{args}"', inline=False)
      
      await chan.send(embed=embed) 
        
      embed=discord.Embed(title="Suggestion Sent", color=0x2F3136)
        
    @commands.command(brief="Price check pokémons")
    async def price(self, ctx, *, pokemon):
        with open('data/price.json') as f:
            prices = json.load(f)
            
        try:
       
            if pokemon.lower().startswith("shiny "):
                shiny = True
                cost = prices[f'{pokemon.title()} ']
                
                species = pokemon[6:]
                
                species = self.bot.data.species_by_name(species)
                
                iv = cost[:-8]
                
                embed=discord.Embed(title=f"Price of Shiny {species}", description=f"Shiny {species} is worth around {iv}", color=0x2F3136)
                embed.set_thumbnail(url=species.shiny_image_url)
                embed.set_footer(text="Note: These prices are based on auctions \nPrices may not be accurate")
                return await ctx.send(embed=embed)
        
            species = self.bot.data.species_by_name(pokemon)
        
            cost = prices[f'{pokemon.title()}']
            price = cost[-6:]#260000 | 32.26%
            iv = cost[:-8]
        
            embed=discord.Embed(title=f"Price of {species}", description=f"{species} with an IV of {price} is worth around {iv}", color=0x2F3136)
            embed.set_thumbnail(url=species.image_url)
            embed.set_footer(text="Note: These prices are based on auctions \nPrices may not be accurate")
            await ctx.send(embed=embed)
        
        except:
            embed=discord.Embed(title=f"{pokemon.title()} not found\nWe are constantly adding prices, maybe try price checking Rare Pokémons or Shiny Pokémons", color=0x2F3136)
            embed.set_footer(text="Note: These prices are based on auctions \nPrices may not be accurate")
            await ctx.send(embed=embed)
      
def setup(bot):
    print("Loaded Commands")
    bot.add_cog(comands(bot))
