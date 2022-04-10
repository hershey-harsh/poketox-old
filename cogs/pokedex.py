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

whitelist = [859326781927194674, 772937584884056135]

allowed = [826928105922232350, 826935014049972265, 797151240173125662, 875526899386953779]

q = ["Xen is made by Future#9409", "Like the bot? Type -invite in the bot's DM", "Want to help? DM Future#9409", "Join the offical server! https://discord.gg/futureworld"]

class Confirm(discord.ui.View):
    def __init__(self, url, species, bot):
        super().__init__()
        self.value = None
        self.url = url
        self.species = species
        self.bot = bot

        url = f"https://discord.com/oauth2/authorize?client_id=875526899386953779&scope=bot%20applications.commands&permissions=388168"

        self.add_item(discord.ui.Button(label="Bot Invite", url=url))

        url = "https://discord.gg/mhcjdJkxn6"

        self.add_item(discord.ui.Button(label="Support Server", url=str(url)))

    @discord.ui.button(label="Dex Info", style=discord.ButtonStyle.gray)
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

    @discord.ui.button(label="Incorrect Prediction", style=discord.ButtonStyle.gray)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Thanks for contributing to the bot! We reported the incorrect prediction to the Owner!", ephemeral=True)
        data = {"content" : f'Reported by: **{interaction.user.name}** *({interaction.user.id})*{self.url}',"username" : "Incorrect Prediction"}

        url = "https://discord.com/api/webhooks/936421747102744666/1UUkTqapNUlsYTZqKkR_s_EL4IwniPL4w9VKlL_QfMh8FV9zwpm0bkUkVsXA3est57T1"

        requests.post(url, json = data)
        self.value = True
        self.stop()

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
    self._unlimited = commands.CooldownMapping.from_cooldown(1, 5.0, commands.BucketType.guild)

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
          embed=discord.Embed(title="<a:loading:875500054868291585> Predicting...", color=0x2f3136)

          aaa = await message.channel.send(embed=embed)
        
          pokemon = solve(img_url)
      
          ctx = await self.bot.get_context(message)
          species = self.bot.data.species_by_name(pokemon)
      
          embed1=discord.Embed(title=pokemon,color=0x2F3136)

          await aaa.edit(embed=embed1, view=Confirm(img_url, pokemon, self.bot))
        
          if species is None:
            return await message.channel.send(f"Could not find a pokemon matching `{species}`.")
          embed1=discord.Embed(title=pokemon,color=0x2F3136)

          if species.description:
              embed1.add_field(name="Description",value= species.description.replace("\n", " "),inline=False)

          embed1.set_thumbnail(url=species.image_url)
          embed1.set_footer(text=f'This server is currently on the {plan} Plan')

          await aaa.edit(embed=embed1)
            
          try:
            await collectors.collectping(self, ctx, species)
            await collectors.shinyping(self, ctx, species)
          except:
            pass

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.embeds and message.author.id == 716390085896962058:
      if "wild" in message.embeds[0].title and message.author.id == 716390085896962058:
        
        free = self.get_ratelimit(message)
        basic = self.get_ratelimit_basic(message)
        premium = self.get_ratelimit_premium(message)
        unlimited = self.get_ratelimit_unlimited(message)
        
        if message.guild.id not in config.basic_premium and config.premium and config.unlimited_premium:
            if free is None:
                await self.identify(message.embeds[0].image.url, message, "Free")
        
        
        elif message.guild.id in config.basic_premium:
            if basic is None:
                await self.identify(message.embeds[0].image.url, message, "Basic")
            
        elif message.guild.id in config.premium:
            if premium is None:
                await self.identify(message.embeds[0].image.url, message, "Premium")
            
        elif message.guild.id in config.unlimited_premium:
            if unlimited is None:
                await self.identify(message.embeds[0].image.url, message, "Unlimited")
        
        else:
            print("Cooldown Hit")
           
                
        
    
def setup(bot):
    print("Loaded Pokedex")
    bot.add_cog(Pokedex(bot))
