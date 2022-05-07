import discord
from discord.ext import commands, menus
from discord.ext import commands, tasks
from helpers.converters import FetchUserConverter, SpeciesConverter
import random
import asyncio
import datetime
from replit import db
from cogs import collectors
import name
import config
import re
from helpers import checks
from discord_webhook import DiscordWebhook, DiscordEmbed
import json
import requests

no_spawn = [844392814485831710, 856328341702836265, 772557819303297054, 849169202966429696]

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

class Confirm(discord.ui.View):
    def __init__(self, url, species, name_poke, bot):
        super().__init__()
        self.value = None
        self.url = url
        self.species = species
        self.bot = bot
        self.name_poke = name_poke
        
    @discord.ui.button(label="Incorrect Prediction", style=discord.ButtonStyle.red, emoji="<:notify:965755380812611614>")
    async def predi(self, interaction: discord.Interaction, button: discord.ui.Button):
                embed=discord.Embed(title="Reported Image", description="Thanks for reporting the image!", color=0x2F3136)

                await interaction.response.send_message(embed=embed,ephemeral=True)
               
                data = {"content" : f'Reported by: **{interaction.user.name}** *({interaction.user.id})* {self.url}',"username" : "Incorrect Prediction"}

                url = "https://discord.com/api/webhooks/936421747102744666/1UUkTqapNUlsYTZqKkR_s_EL4IwniPL4w9VKlL_QfMh8FV9zwpm0bkUkVsXA3est57T1"

                requests.post(url, json = data)
        
    @discord.ui.button(label="Dex Info", style=discord.ButtonStyle.blurple, emoji="<:pokedex:965752930789621810>")
    async def info(self, interaction: discord.Interaction, button: discord.ui.Button):

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
    self.daily_task.start()
    self._free = commands.CooldownMapping.from_cooldown(1, 15.0, commands.BucketType.guild)

  def get_ratelimit(self, message):
        bucket = self._free.get_bucket(message)
        return bucket.update_rate_limit()
    
  async def premium_identify(self, img_url, message, plan):
    
          ctx = await self.bot.get_context(message)
          guild = await ctx.bot.mongo.fetch_guild(ctx.guild)
    
          try:
                allow_mode = guild["name"]
          except: 
                allow_mode = "On"
                
          if allow_mode == "Off":
                pokemon = name.identifyy(img_url)
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
        
        
          pokemon = name.identifyy(img_url)
      
          species = self.bot.data.species_by_name(pokemon)
        
          embed1=discord.Embed(title=pokemon, description=f"The pokémon spawned is {pokemon}\nNeed help? Join our [Support Server](https://discord.gg/YmVA2ah5tE)", color=0x2F3136)

          embed1.set_thumbnail(url=species.image_url)
          embed1.set_footer(text=f'This server is currently on the {plan} Plan')
        
          await message.reply(embed=embed1, view=Confirm(img_url, pokemon, pokemon, self.bot))
                
          try:
                await collectors.collectping(self, ctx, species)
                await collectors.shinyping(self, ctx, species)
          except:
                pass
            
          total_count = spawn_count + 1

          await self.bot.mongo.update_guild(
                    ctx.guild, {"$set": {"spawn_count": str(total_count)}}
          )
        
          if pokemon in rare_pokes:
                        
                ctx = await self.bot.get_context(message)
                guild = await ctx.bot.mongo.fetch_guild(ctx.guild)

                try:
                    roleid = guild["rareping"]
                    await message.channel.send(f'<@&{roleid}>')
                
                except:
                    pass
    
  async def identify(self, img_url, message, plan):
    
    ctx = await self.bot.get_context(message)
    guild = await ctx.bot.mongo.fetch_guild(ctx.guild)
    
    try:
        spawn_count = int(guild["spawn_count"])
    except:
        spawn_count = 0
    
    if spawn_count >=750:
        return
    
    else:
    
          try:
                allow_mode = guild["name"]
          except: 
                allow_mode = "On"
                
          if allow_mode == "Off":
                pokemon = name.identifyy(img_url)
                species = self.bot.data.species_by_name(pokemon)
                ctx = await self.bot.get_context(message)
                await collectors.collectping(self, ctx, species)
                await collectors.shinyping(self, ctx, species)
                
                total_count = spawn_count + 1

                await self.bot.mongo.update_guild(
                        ctx.guild, {"$set": {"spawn_count": str(total_count)}}
                )
                
                if pokemon in rare_pokes:
                        
                        ctx = await self.bot.get_context(message)
                        guild = await ctx.bot.mongo.fetch_guild(ctx.guild)

                        try:
                                roleid = guild["rareping"]
                                await message.channel.send(f'<@&{roleid}>')
                
                        except:
                                pass
                return
        
        
          pokemon = name.identifyy(img_url)
      
          species = self.bot.data.species_by_name(pokemon)
        
          embed1=discord.Embed(title=pokemon, description=f"The pokémon spawned is {pokemon}\nNeed help? Join our [Support Server](https://discord.gg/YmVA2ah5tE)", color=0x2F3136)

          embed1.set_thumbnail(url=species.image_url)
          embed1.set_footer(text=f'This server is currently on the {plan} Plan')
        
          await message.reply(embed=embed1, view=Confirm(img_url, pokemon, pokemon, self.bot))
                
          try:
                await collectors.collectping(self, ctx, species)
                await collectors.shinyping(self, ctx, species)
          except:
                pass
            
          total_count = spawn_count + 1

          await self.bot.mongo.update_guild(
                    ctx.guild, {"$set": {"spawn_count": str(total_count)}}
          )
        
          if pokemon in rare_pokes:
                        
                ctx = await self.bot.get_context(message)
                guild = await ctx.bot.mongo.fetch_guild(ctx.guild)

                try:
                    roleid = guild["rareping"]
                    await message.channel.send(f'<@&{roleid}>')
                
                except:
                    pass
  @checks.has_started()           
  @commands.group(invoke_without_command=True)
  async def toggle(self, ctx):
                return None
        
  @checks.has_started()
  @toggle.group(invoke_without_command=True)
  async def spawn(self, ctx):
                return None
    
  @checks.has_started()
  @spawn.command()
  async def enable(self, ctx):
        mode = "On"
        
        await self.bot.mongo.update_guild(
            ctx.guild, {"$set": {"name": str(mode)}}
        )
        
        embed=discord.Embed(title="Spawn", description="I will start identifying spawn images", color=0x36393F)
        await ctx.send(embed=embed)
  
  @checks.has_started()
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
    
    if message.channel.id == 969956361616109578 and message.author.id != 875526899386953779:
          pokemon = name.identifyy(message.content)
          species = self.bot.data.species_by_name(pokemon)
          embed1=discord.Embed(title=pokemon, description=f"The pokémon spawned is {pokemon}\nNeed help? Join our [Support Server](https://discord.gg/YmVA2ah5tE)", color=0x2F3136)

          embed1.set_thumbnail(url=species.image_url)
        
          await message.reply(embed=embed1, view=Confirm(message.content, pokemon, pokemon, self.bot))
        

    if message.author.id == 716390085896962058 and "The pokémon is" in message.content:
        solution = hint_solve(message.content)
   
        embed1=discord.Embed(title=solution[0].capitalize(), description=f"The pokémon spawned is {solution[0]}\nNeed help? Join our [Support Server](https://discord.gg/mhcjdJkxn6)", color=0x2F3136)
        species = self.bot.data.species_by_name(solution[0])
        embed1.set_thumbnail(url=species.image_url)
        await message.channel.send(embed=embed1)
        
  
        
    if message.embeds and message.author.id == 716390085896962058:
      if "wild" in message.embeds[0].title:
        
        free = self.get_ratelimit(message)
        
        total_servers = config.basic_premium + config.premium + config.unlimited_premium
        val = (message.guild.id in total_servers)
        
        if val == False:
            if free is None:
                await self.identify(message.embeds[0].image.url, message, "Free")
            else:
                return
        
        elif message.guild.id in config.basic_premium:
            if basic is None:
                await self.premium_identify(message.embeds[0].image.url, message, "Basic")
            else:
                embed=discord.Embed(title=":x: Cooldown Reached", description=f"`{int(basic)}` seconds left till Cooldown expires\nYour current plan is **Premium**, you can upgrade your plan at https://poketox.me/pricing", color=0x2f3136)

                embed.set_footer(text="Did you know if your server has over 10k members you get free Premium! DM Future#0811 to claim your free premium")
                await message.channel.send(embed=embed)
            
        elif message.guild.id in config.premium:
            if premium is None:
                await self.premium_identify(message.embeds[0].image.url, message, "Premium")
            else:
                embed=discord.Embed(title=":x: Cooldown Reached", description=f"`{int(premium)}` seconds left till Cooldown expires \nYour current plan is **Premium**, you can upgrade your plan at https://poketox.me/pricing", color=0x2f3136)
                
                await message.channel.send(embed=embed)
            
        elif message.guild.id in config.unlimited_premium:
                await self.premium_identify(message.embeds[0].image.url, message, "Unlimited")
           
  time_to_execute_task = datetime.time(hour=4, minute=0)    
            
  @tasks.loop(time=time_to_execute_task)
  async def daily_task(self):
        await self.bot.mongo.db.guild.update_many(
            {},
            {"$set": {"spawn_count": "0"}},
        )
        
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/970282274933338143/redztJ-2YtovCko_kJ1IGG3flPN8VdEXJiq6-rlXzHui_xDrOiDjU2WewncMKzBKPlE2')
        
        embed = DiscordEmbed(title='Naming Reset', description='Pokétox has reset the Naming Count back to 0. Pokétox will name 750 pokémons as a part of the free plan', color='03b2f8')
        webhook.add_embed(embed)

        webhook.execute()
    
async def setup(bot):
    print("Loaded Pokedex")
    await bot.add_cog(Pokedex(bot))
