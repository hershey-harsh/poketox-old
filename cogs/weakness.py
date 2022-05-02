import discord
from discord.ext import commands, menus
import random
import asyncio
import datetime
from replit import db
import requests
import json
import psutil
from similar import Similar
import os
from discord.ext.commands import cooldown, BucketType
from helpers import checks

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

all_types = ["bug", "dark", "dragon", "electric", "fairy", "fighting", "fire", "flying", "ghost", "grass", "ground", "ice", "normal", "poison", "psychic", "rock", "steel", "water"]

class Weakness(commands.Cog):

    """Weakness data Manager"""

    def __init__(self, bot):
        self.bot = bot
        
    @checks.has_started()
    @commands.guild_only()
    @commands.hybrid_command(description="View a pokémons weakness")
    async def weakness(self, ctx, *, pokemon):
        vote=voted(ctx.author.id)
        if vote == False:
                embed=discord.Embed(title="Vote Required", description="Please vote for Pokétox below before using this command", color=0x2F3136)
                embed.add_field(name="Vote for the bot", value="[Top.gg bot voting](https://top.gg/bot/875526899386953779/vote)", inline=True)
                return await ctx.send(embed=embed)
            
        params = pokemon

        params = [p.lower() for p in params]

        # determine the type of input
        type_input = False

        type_input = False

        # return if input error
        if type_input:
            for t in params:
                if t.lower() not in all_types:
                    return
        else:
            if len(params) > 1:
                return

        try:
            if not type_input:
              with open('data/type_data.json') as f:
                data0 = json.load(f)
                types = data0[params[0]]
            else:
                types = params
        except KeyError as err:
            await ctx.send("Pokemon not found")
            return

        # get individual weakness per type
        individual_weakness = {}

        for type in types:
              with open('data/weakness_data.json') as f:
                data1 = json.load(f)
              individual_weakness[type.lower()] = data1[type.lower()]

        # get overall weakness after multiplying the individual weaknesses
        overall_weakness = {"bug": 1, "dark": 1, "dragon": 1, "electric": 1, "fairy": 1, "fighting": 1, "fire": 1, "flying": 1, "ghost": 1, "grass": 1, "ground": 1, "ice": 1, "normal": 1, "poison": 1, "psychic": 1, "rock": 1, "steel": 1, "water": 1}

        for i in list(individual_weakness.keys()):
            for j in all_types:
                overall_weakness[j] = overall_weakness[j] * individual_weakness[i][j]

        # divide the overall weaknesses into tiers
        weakness_tiers = {"super weak" : "", "weak" : "", "neutral" : "", "resistive" : "", "super resistive" : "","immune" : ""}

        for type in list(overall_weakness.keys()):
            if overall_weakness[type] > 2:
                weakness_tiers["super Weakness"] = weakness_tiers["super weak"] + type.title() + " - "
            elif overall_weakness[type] > 1:
                weakness_tiers["weakness"] = weakness_tiers["weak"] + type.title() + " - "
            elif overall_weakness[type] == 1:
                weakness_tiers["neutral"] = weakness_tiers["neutral"] + type.title() + " - "
            elif overall_weakness[type] > 0.5:
                weakness_tiers["resistive"] = weakness_tiers["resistive"] + type.title() + " - "
            elif overall_weakness[type] > 0:
                weakness_tiers["super Resistive"] = weakness_tiers["super resistive"] + type.title() + " - "
            else:
                weakness_tiers["immune"] = weakness_tiers["immune"] + type.title() + " - "

        # prepare the embed heading
        heading = ""

        if type_input:
            for i in types:
                heading += f"{i.capitalize()} "
        else:
            heading = f"{params[0].capitalize()} is an"
            for i in types:
                heading += f" **{i.capitalize()} **/"

        # prepare and send the embed
        embed = discord.Embed(title=f"{pokemon[0].capitalize()}'s Weakness",description=f"{heading[:-1]} type. ", color=0x2F3136)

        species = pokemon

        species = self.bot.data.species_by_name(species[0])

        for tier in list(weakness_tiers.keys()):
            
            if len(weakness_tiers[tier]) <= 0:
                continue
            stuff = str(weakness_tiers[tier][:-2].replace("-", "|"))
            embed.add_field(
                name=f"{tier.capitalize()}",
                value=f'```{stuff.title()}```',
                inline=False
            )

        await ctx.send(embed=embed, ephemeral=False)

async def setup(bot):
    print("Loaded Weakness")
    await bot.add_cog(Weakness(bot))
