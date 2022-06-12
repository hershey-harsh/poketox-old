import discord
from discord.ext import commands
from helpers import checks
from helpers.converters import FetchUserConverter, SpeciesConverter
import config
import json
import requests
from typing import Literal
from similar import best_match

with open('data/price.json') as f:
        prices = json.load(f)

def voted(userid):
        headers = {'authorization': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijg3NTUyNjg5OTM4Njk1Mzc3OSIsImJvdCI6dHJ1ZSwiaWF0IjoxNjUwNDE0MjMzfQ.7aZSEjaVH-lH-KtBe_Q2pmGA-wnbyLLbODxEhcfghAE", 'content-type': 'application/json'}

        url = f"https://top.gg/api/bots/875526899386953779/check?userId={userid}"
        response = requests.get(url, headers=headers)
        
        output = json.loads(response.text)
        vote = output['voted']
        
        vote = str(vote)
        
        if vote == "1":
                return True
        else:
                return False

async def get_nature_embed(poke):
        with open('data/nature.json') as f:
          nature = json.load(f)
        mature = nature[poke.name.lower()]

        embd=discord.Embed(title=f"{poke.capitalize()}'s Nature", description=f"The best nature of {poke}.", color=0x2F3136)

        embd.add_field(name="Nature", value=f"```{mature}```", inline=False)
  
        return embd

async def get_moveset_embed(poke):

        with open('data/moveset.json') as f:
          movese = json.load(f)
        ms = movese[poke.name.lower()]

        embd=discord.Embed(title=f"{poke.capitalize()}'s Moveset", description="The more **HP, Defense, Speed Defense, Speed** the better chance of winning battles.", color=0x2F3136)

        embd.add_field(name="Moveset", value=f"```{ms}```", inline=False)

        return embd

async def get_stats_embed(pokemon):

        with open('data/stats.json') as f:
          pokes = json.load(f)
        name = pokes[pokemon.name.lower()]

        embd=discord.Embed(title=f"{pokemon.capitalize()}'s Stats", description="The more **HP, Defense, Speed Defense, Speed** the better stats.", color=0x2F3136)

        embd.add_field(name="Stats", value=f"```{name}```", inline=False)

        return embd

class stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.has_started()
    @commands.hybrid_command(brief="Shows shiny rate of a pokémon")
    async def nature(self, ctx, pokemon):
        vote=voted(ctx.author.id)
        if vote == False:
                embed=discord.Embed(title="Vote Required", description="Please vote for Pokétox below before using this command", color=0x2F3136)
                embed.add_field(name="Vote for the bot", value="[Top.gg bot voting](https://top.gg/bot/875526899386953779/vote)", inline=True)
                return await ctx.send(embed=embed)
        pokemon = self.bot.data.species_by_name(pokemon)
        reply = await get_nature_embed(pokemon)
        await ctx.send(embed=reply)
  
    @checks.has_started()
    @commands.hybrid_command()
    async def stats(self, ctx, pokemon):
        """Shows statistics needed for an duelish pokémon"""
        vote=voted(ctx.author.id)
        if vote == False:
                embed=discord.Embed(title="Vote Required", description="Please vote for Pokétox below before using this command", color=0x2F3136)
                embed.add_field(name="Vote for the bot", value="[Top.gg bot voting](https://top.gg/bot/875526899386953779/vote)", inline=True)
                return await ctx.send(embed=embed)
        pokemon = self.bot.data.species_by_name(pokemon)
        reply = await get_stats_embed(pokemon)
        await ctx.reply(embed=reply)

    @checks.has_started()
    @commands.hybrid_command()
    async def moveset(self, ctx, pokemon):
        """Shows the pokémons moves"""
        vote=voted(ctx.author.id)
        if vote == False:
                embed=discord.Embed(title="Vote Required", description="Please vote for Pokétox below before using this command", color=0x2F3136)
                embed.add_field(name="Vote for the bot", value="[Top.gg bot voting](https://top.gg/bot/875526899386953779/vote)", inline=True)
                return await ctx.send(embed=embed)
        pokemon = self.bot.data.species_by_name(pokemon)
        reply = await get_moveset_embed(pokemon)
        await ctx.reply(embed=reply)

    @checks.has_started()
    @commands.hybrid_command(brief="Shows estimated price of the pokémon")
    async def price(self, ctx, *, pokemon):
        vote=voted(ctx.author.id)
        if vote == False:
                embed=discord.Embed(title="Vote Required", description="Please vote for Pokétox below before using this command", color=0x2F3136)
                embed.add_field(name="Vote for the bot", value="[Top.gg bot voting](https://top.gg/bot/875526899386953779/vote)", inline=True)
                return await ctx.send(embed=embed)
            
        try:
       
            if pokemon.lower().startswith("shiny "):
                shiny = True
                cost = prices[f'{pokemon.title()} ']
                
                species = pokemon[6:]
                
                species = self.bot.data.species_by_name(species)
                
                iv = cost[:-8]
                
                iv = "{:,}".format(int(iv))
                
                embed=discord.Embed(title=f"Price of Shiny {species}", description=f"Shiny {species} is worth around {iv}", color=0x2F3136)
                embed.set_thumbnail(url=species.shiny_image_url)
                embed.set_footer(text="These prices are based on auctions\nNote: Prices may not be accurate")
                return await ctx.send(embed=embed)
        
            species = self.bot.data.species_by_name(pokemon)
        
            cost = prices[f'{pokemon.title()}']
            price = cost[-6:]#260000 | 32.26%
            iv = cost[:-8]
            
            iv = "{:,}".format(int(iv))
        
            embed=discord.Embed(title=f"Price of {species}", description=f"{species} with an IV of {price} is worth around {iv}", color=0x2F3136)
            embed.set_thumbnail(url=species.image_url)
            embed.set_footer(text="These prices are based on auctions \nNote: Prices may not be accurate")
            await ctx.send(embed=embed)
        
        except:
            embed=discord.Embed(title=f"{pokemon.title()} not found", description=f'We are constantly adding prices, maybe try price checking Rare Pokémons or Shiny Pokémons', color=0x2F3136)
            embed.add_field(name="Maybe you meant?", value=best_match(pokemon, prices.keys()))
            embed.set_footer(text="These prices are based on auctions\nNote: Prices may not be accurate")
            await ctx.send(embed=embed)

async def setup(bot):
    print("Loaded Info")
    await bot.add_cog(stats(bot))
