import discord
from discord.ext import commands, menus
from helpers.converters import FetchUserConverter, SpeciesConverter
import random
import asyncio
import datetime
from replit import db
from cogs import collectors
from name import solve
import config
import re

import json
import requests

no_spawn = [844392814485831710, 856328341702836265, 772557819303297054, 849169202966429696]

async def get_stats_embed(pokemon):

        with open('data/stats.json') as f:
          pokes = json.load(f)
        name = pokes[pokemon.lower()]

        embd=discord.Embed(title=f"{pokemon.capitalize()}'s Stats", description="The more **HP, Defense, Speed Defense, Speed** the better stats.", color=0x2F3136)

        embd.add_field(name="Stats", value=f"```{name}```", inline=False)

        return embd

with open("pokemon.txt","r",encoding="utf8") as file:
    pokemon_list_string = file.read()
    
with open("rare.txt","r",encoding="utf8") as file:
    rare_pokes = file.read()

whitelist = [859326781927194674, 772937584884056135]

allowed = [826928105922232350, 826935014049972265, 797151240173125662, 875526899386953779]

q = ["Xen is made by Future#9409", "Like the bot? Type -invite in the bot's DM", "Want to help? DM Future#9409", "Join the offical server! https://discord.gg/futureworld"]

def hint_solve(message):
    hint = []

    for i in range(15,len(message) - 1):
        if message[i] != "\\":
            hint.append(message[i])

    hint_string = ""
    for i in hint:
        hint_string += i
        
    hint_replaced = hint_string.replace("_",".")
    solution = re.findall('^'+hint_replaced+'$',pokemon_list_string, re.MULTILINE)
    return solution

class Confirmm(discord.ui.View):
    def __init__(self, url, species, name_poke, bot):
        super().__init__()
        self.value = None
        self.url = url
        self.species = species
        self.bot = bot
        self.name_poke = name_poke

    @discord.ui.button(label="Dex Info", style=discord.ButtonStyle.blurple)
    async def info(self, button: discord.ui.Button, interaction: discord.Interaction):

        species = self.species
      
        if species.isdigit():
            species = self.bot.data.species_by_number(int(species))
        else:
            if species.lower().startswith("shiny "):
                shiny = True
                species = species[6:]

            species = self.bot.data.species_by_name(species)

        embed = discord.Embed(color=0x2F3136)
        embed.title = f"#{species.dex_number} — {species}"

        if species.description:
            embed.description = species.description.replace("\n", " ")

        # Pokemon Rarity
        rarity = []
        if species.mythical:
            rarity.append("Mythical")
        if species.legendary:
            rarity.append("Legendary")
        if species.ultra_beast:
            rarity.append("Ultra Beast")
        if species.event:
            rarity.append("Event")

        if rarity:
            rarity = ", ".join(rarity)
            embed.add_field(
                name="Rarity",
                value=rarity,
                inline=False,
            )

        if species.evolution_text:
            embed.add_field(name="Evolution", value=species.evolution_text, inline=False)

        if 1 == 2:
            print("idk")
        else:
            embed.set_thumbnail(url=species.image_url)

        base_stats = (
            f"**HP:** {species.base_stats.hp}",
            f"**Attack:** {species.base_stats.atk}",
            f"**Defense:** {species.base_stats.defn}",
            f"**Sp. Atk:** {species.base_stats.satk}",
            f"**Sp. Def:** {species.base_stats.sdef}",
            f"**Speed:** {species.base_stats.spd}",
        )

        embed.add_field(
            name="Names",
            value="\n".join(f"{x} {y}" for x, y in species.names),
        )
        embed.add_field(name="Base Stats", value="\n".join(base_stats))
        embed.add_field(name="Types", value="\n".join(species.types))

        await interaction.response.send_message(embed=embed,ephemeral=True)
        
    @discord.ui.button(label="Stats", style=discord.ButtonStyle.blurple, disabled=True)
    async def stats(self, button: discord.ui.Button, interaction: discord.Interaction):
        reply = await get_stats_embed(self.name_poke)
        await interaction.response.send_message(embed=reply,ephemeral=True)

class Confirm(discord.ui.View):
    def __init__(self, url, species, name_poke, bot):
        super().__init__()
        self.value = None
        self.url = url
        self.species = species
        self.bot = bot
        self.name_poke = name_poke

    @discord.ui.button(label="Dex Info", style=discord.ButtonStyle.blurple)
    async def info(self, button: discord.ui.Button, interaction: discord.Interaction):

        species = self.species
      
        if species.isdigit():
            species = self.bot.data.species_by_number(int(species))
        else:
            if species.lower().startswith("shiny "):
                shiny = True
                species = species[6:]

            species = self.bot.data.species_by_name(species)

        embed = discord.Embed(color=0x2F3136)
        embed.title = f"#{species.dex_number} — {species}"

        if species.description:
            embed.description = species.description.replace("\n", " ")

        # Pokemon Rarity
        rarity = []
        if species.mythical:
            rarity.append("Mythical")
        if species.legendary:
            rarity.append("Legendary")
        if species.ultra_beast:
            rarity.append("Ultra Beast")
        if species.event:
            rarity.append("Event")

        if rarity:
            rarity = ", ".join(rarity)
            embed.add_field(
                name="Rarity",
                value=rarity,
                inline=False,
            )

        if species.evolution_text:
            embed.add_field(name="Evolution", value=species.evolution_text, inline=False)

        if 1 == 2:
            print("idk")
        else:
            embed.set_thumbnail(url=species.image_url)

        base_stats = (
            f"**HP:** {species.base_stats.hp}",
            f"**Attack:** {species.base_stats.atk}",
            f"**Defense:** {species.base_stats.defn}",
            f"**Sp. Atk:** {species.base_stats.satk}",
            f"**Sp. Def:** {species.base_stats.sdef}",
            f"**Speed:** {species.base_stats.spd}",
        )

        embed.add_field(
            name="Names",
            value="\n".join(f"{x} {y}" for x, y in species.names),
        )
        embed.add_field(name="Base Stats", value="\n".join(base_stats))
        embed.add_field(name="Types", value="\n".join(species.types))

        await interaction.response.send_message(embed=embed,ephemeral=True)
        
    @discord.ui.button(label="Stats", style=discord.ButtonStyle.blurple, disabled=True)
    async def stats(self, button: discord.ui.Button, interaction: discord.Interaction):
        reply = await get_stats_embed(self.name_poke)
        await interaction.response.send_message(embed=reply,ephemeral=True)

import requests
import json
import psutil
from similar import Similar
import os
from discord.ext.commands import cooldown, BucketType

class Pokedex(commands.Cog):
  """Check pokedex."""

  def __init__(self, bot):
    self.bot = bot
    self._free = commands.CooldownMapping.from_cooldown(1, 120.0, commands.BucketType.guild)
    self._basic = commands.CooldownMapping.from_cooldown(1, 60.0, commands.BucketType.guild)
    self._premium = commands.CooldownMapping.from_cooldown(1, 30.0, commands.BucketType.guild)
    self._unlimited = commands.CooldownMapping.from_cooldown(1, 1.0, commands.BucketType.guild)

  def get_ratelimit(self, message):
        bucket = self._free.get_bucket(message)
        return bucket.update_rate_limit()

  def get_ratelimit_basic(self, message):
        bucket = self._basic.get_bucket(message)
        return bucket.update_rate_limit()
    
  def get_ratelimit_premium(self, message):
        bucket = self._premium.get_bucket(message)
        return bucket.update_rate_limit()
    
  def get_ratelimit_unlimited(self, message):
        bucket = self._unlimited.get_bucket(message)
        return bucket.update_rate_limit()
    
  async def identify(self, img_url, message, plan):
          ctx = await self.bot.get_context(message)
          guild = await ctx.bot.mongo.fetch_guild(ctx.guild)
          
          try:
                allow_mode = guild["name"]
          except: 
                allow_mode = "On"
                
          if allow_mode == "Off":
                pokemon = solve(img_url)
                species = self.bot.data.species_by_name(pokemon)
                ctx = await self.bot.get_context(message)
                await collectors.collectping(self, ctx, species)
                await collectors.shinyping(self, ctx, species)
                if pokemon in rare_pokes:
                        
                        ctx = await self.bot.get_context(message)
                        guild = await ctx.bot.mongo.fetch_guild(ctx.guild)

                        try:
                                roleid = guild["rareping"]
                                await message.channel.send(f'<@&{roleid}>')
                
                        except:
                                pass
                return
        
          embed=discord.Embed(title="<a:loading:875500054868291585> Predicting...", color=0x2f3136)
          
          aaa = await message.channel.send(embed=embed)
        
          pokemon = solve(img_url)
      
          species = self.bot.data.species_by_name(pokemon)
        
          if species is None:
            return await message.channel.send(f"Could not find a pokemon matching `{species}`.")
          embed1=discord.Embed(title=pokemon, description="Need help? Join our [Support Server](https://discord.gg/mhcjdJkxn6) \nWant my invite link? Invite the bot [here](https://discord.gg/mhcjdJkxn6)", color=0x2F3136)

          embed1.set_thumbnail(url=species.image_url)
          embed1.set_footer(text=f'This server is currently on the {plan} Plan')
        
          await aaa.edit(embed=embed1, view=Confirm(img_url, pokemon, pokemon, self.bot))
                
          try:
                await collectors.collectping(self, ctx, species)
                await collectors.shinyping(self, ctx, species)
          except:
                pass
        
          if pokemon in rare_pokes:
                        
                ctx = await self.bot.get_context(message)
                guild = await ctx.bot.mongo.fetch_guild(ctx.guild)

                try:
                    roleid = guild["rareping"]
                    await message.channel.send(f'<@&{roleid}>')
                
                except:
                    pass
                
  @commands.group(invoke_without_command=True)
  async def toggle(self, ctx):
                return None
        
  @toggle.group(invoke_without_command=True)
  async def spawn(self, ctx):
                return None
        
  @spawn.command()
  async def enable(self, ctx):
        mode = "On"
        
        await self.bot.mongo.update_guild(
            ctx.guild, {"$set": {"name": str(mode)}}
        )
        
        embed=discord.Embed(title="Spawn", description="I will start identifying spawn images", color=0x36393F)
        await ctx.send(embed=embed)
  @commands.has_permissions(manage_messages=True)     
  @spawn.command()
  async def disable(self, ctx):
        mode = "Off"
        
        await self.bot.mongo.update_guild(
            ctx.guild, {"$set": {"name": str(mode)}}
        )
        
        embed=discord.Embed(title="Spawn", description="I will stop identifying spawn images", color=0x36393F)
        await ctx.send(embed=embed)
  @commands.has_permissions(manage_messages=True)            
  @commands.Cog.listener()
  async def on_message(self, message):

    if message.author.id == 716390085896962058 and "The pokémon is" in message.content:
        solution = hint_solve(message.content)
   
        embed = discord.Embed(color=0x2F3136)
        embed.title = f"{solution}"
        await message.channel.send(embed=embed)
        
    if message.embeds and message.author.id == 716390085896962058:
      if "wild" in message.embeds[0].title:
        
        free = self.get_ratelimit(message)
        basic = self.get_ratelimit_basic(message)
        premium = self.get_ratelimit_premium(message)
        unlimited = self.get_ratelimit_unlimited(message)
        
        total_servers = config.basic_premium + config.premium + config.unlimited_premium
        val = (message.guild.id in total_servers)
        if val == False:
            if free is None:
                await self.identify(message.embeds[0].image.url, message, "Free")
            else:
                embed=discord.Embed(title=":x: Cooldown Reached", description=f"`{int(free)}` seconds left till Cooldown expires", color=0x2f3136)
                embed.add_field(name="Tired of cooldowns?", value="You can support the bot by buying one of our many plans at https://poketox.me/pricing", inline=False)
                embed.set_footer(text="Did you know if your server has over 10k members you get free Premium! DM Future#0811 to claim your free premium")
                await message.channel.send(embed=embed)
        
        elif message.guild.id in config.basic_premium:
            if basic is None:
                await self.identify(message.embeds[0].image.url, message, "Basic")
            else:
                embed=discord.Embed(title=":x: Cooldown Reached", description=f"`{int(basic)}` seconds left till Cooldown expires", color=0x2f3136)
                embed.add_field(name="Tired of cooldowns?", value="Your current plan is **Basic**, you can upgrade your plan at https://poketox.me/pricing", inline=False)
                embed.set_footer(text="Did you know if your server has over 10k members you get free Premium! DM Future#0811 to claim your free premium")
                await message.channel.send(embed=embed)
            
        elif message.guild.id in config.premium:
            if premium is None:
                await self.identify(message.embeds[0].image.url, message, "Premium")
            else:
                embed=discord.Embed(title=":x: Cooldown Reached", description=f"`{int(premium)}` seconds left till Cooldown expires", color=0x2f3136)
                embed.add_field(name="Tired of cooldowns?", value="Your current plan is **Premium**, you can upgrade your plan at https://poketox.me/pricing", inline=False)
                embed.set_footer(text="Did you know if your server has over 10k members you get free Premium! DM Future#0811 to claim your free premium")
                await message.channel.send(embed=embed)
            
        elif message.guild.id in config.unlimited_premium:
            if unlimited is None:
                await self.identify(message.embeds[0].image.url, message, "Unlimited")
            else:
                embed=discord.Embed(title=":x: Cooldown Reached", description=f"`{int(unlimited)}` seconds left till Cooldown expires", color=0x2f3136)
                await message.channel.send(embed=embed)
           
                
        
    
def setup(bot):
    print("Loaded Pokedex")
    bot.add_cog(Pokedex(bot))
