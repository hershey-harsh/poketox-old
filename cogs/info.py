import discord
from discord.ext import commands
import config
import json
import requests
from typing import Literal

async def get_nature_embed(poke: str):
        with open('data/nature.json') as f:
          nature = json.load(f)
        mature = nature[poke.lower()]

        embd=discord.Embed(title=f"{poke.capitalize()}'s Nature", description=f"The best nature of {poke}.", color=0x2F3136)

        embd.add_field(name="Nature", value=f"```{mature}```", inline=False)
  
        return embd

async def get_moveset_embed(poke):

        with open('data/moveset.json') as f:
          movese = json.load(f)
        ms = movese[poke.lower()]

        embd=discord.Embed(title=f"{poke.capitalize()}'s Moveset", description="The more **HP, Defense, Speed Defense, Speed** the better chance of winning battles.", color=0x2F3136)

        embd.add_field(name="Moveset", value=f"```{ms}```", inline=False)

        return embd

async def get_stats_embed(pokemon):

        with open('data/stats.json') as f:
          pokes = json.load(f)
        name = pokes[pokemon.lower()]

        embd=discord.Embed(title=f"{pokemon.capitalize()}'s Stats", description="The more **HP, Defense, Speed Defense, Speed** the better stats.", color=0x2F3136)

        embd.add_field(name="Stats", value=f"```{name}```", inline=False)

        return embd

class stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def nature(self, ctx, poke : str):
        reply = await get_nature_embed(poke)
        await ctx.send(embed=reply)
  
    @commands.command()
    async def stats(self, ctx, pokemon:str):
        """Shows statistics needed for an duelish pokémon"""
        reply = await get_stats_embed(pokemon)
        await ctx.reply(embed=reply)

    @commands.command()
    async def moveset(self, ctx, pokemon):
        """Shows the pokémons moves"""
        reply = await get_moveset_embed(pokemon)
        await ctx.reply(embed=reply)





def setup(bot):
    print("Loaded Info")
    bot.add_cog(stats(bot))
