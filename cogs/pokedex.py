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
    self._free = commands.CooldownMapping.from_cooldown(1, 30.0, commands.BucketType.guild)

  def get_ratelimit(self, message):
        bucket = self._free.get_bucket(message)
        return bucket.update_rate_limit()
    
  async def premium_identify(self, img_url, message, plan):
    ctx = await self.bot.get_context(message)
    guild = await ctx.bot.mongo.fetch_guild(ctx.guild)
    
    try:
        spawn_count = int(guild["spawn_count"])
    except:
        spawn_count = 0
    
    if spawn_count >=5000:
        return
    
    else:
    
          ctx = await self.bot.get_context(message)
          guild = await ctx.bot.mongo.fetch_guild(ctx.guild)
    
          try:
                allow_mode = guild["name"]
          except: 
                allow_mode = "On"
                
          if allow_mode == "Off":
                pokemon = await name.identifyy(img_url)
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
        
        
          pokemon = await name.identifyy(img_url)
      
          species = self.bot.data.species_by_name(pokemon)
        
          embed1=discord.Embed(title=pokemon, description=f"The pokémon spawned is {pokemon}\nNeed help? Join our [Support Server](https://discord.gg/YmVA2ah5tE)", color=0x2F3136)

          embed1.set_thumbnail(url=species.image_url)
          embed1.set_footer(text=f'This server is currently on the {plan} Plan')
        
          #await message.reply(embed=embed1, view=Confirm(img_url, pokemon, pokemon, self.bot))
          await message.reply(embed=embed1)

          if pokemon in rare_pokes:
                        
                ctx = await self.bot.get_context(message)
                guild = await ctx.bot.mongo.fetch_guild(ctx.guild)

                try:
                    roleid = guild["rareping"]
                    await message.channel.send(f'<@&{roleid}>')
                
                except:
                    pass
                
          try:
                await collectors.shinyping(self, ctx, species)
                await collectors.collectping(self, ctx, species)
          except:
                pass

          await self.bot.mongo.update_guild(
                    ctx.guild, {"$set": {"spawn_count": str(total_count)}}
          )
    
  async def identify(self, img_url, message, plan):
    
    ctx = await self.bot.get_context(message)
    guild = await ctx.bot.mongo.fetch_guild(ctx.guild)
    
    try:
        spawn_count = int(guild["spawn_count"])
    except:
        spawn_count = 0
    
    #if spawn_count >=750:
    if spawn_count >= 2000:
        return
    
    else:
    
          try:
                allow_mode = guild["name"]
          except: 
                allow_mode = "On"
                
          if allow_mode == "Off":
                pokemon = await name.identifyy(img_url)
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
        
        
          pokemon = await name.identifyy(img_url)
      
          species = self.bot.data.species_by_name(pokemon)
        
          embed1=discord.Embed(title=pokemon, description=f"The pokémon spawned is {pokemon}\nNeed help? Join our [Support Server](https://discord.gg/YmVA2ah5tE)", color=0x2F3136)

          embed1.set_thumbnail(url=species.image_url)
          embed1.set_footer(text=f'This server is currently on the {plan} Plan')
        
          #await message.reply(embed=embed1, view=Confirm(img_url, pokemon, pokemon, self.bot))
          await message.reply(embed=embed1)
        
          if pokemon in rare_pokes:
                        
                ctx = await self.bot.get_context(message)
                guild = await ctx.bot.mongo.fetch_guild(ctx.guild)

                try:
                    roleid = guild["rareping"]
                    await message.channel.send(f'<@&{roleid}>')
                
                except:
                    pass
                
          try:
                await collectors.shinyping(self, ctx, species)
                await collectors.collectping(self, ctx, species)
          except:
                pass
            
          total_count = spawn_count + 1

          await self.bot.mongo.update_guild(
                    ctx.guild, {"$set": {"spawn_count": str(total_count)}}
          )
            
          guild = await ctx.bot.mongo.fetch_total_count(ctx.guild)
          
          try:
            total_count = int(guild["total_count"])
          except:
            total_count = 0
            
          await self.bot.mongo.update_total_count(
                    ctx.guild, {"$set": {"total_count": str(total_count+1)}}
          )
        
  @commands.has_permissions(manage_messages=True)            
  @commands.Cog.listener()
  async def on_message(self, message):
    
    if message.channel.id == 969956361616109578 and message.author.id != 875526899386953779:
          pokemon = await name.identifyy(message.content)
          species = self.bot.data.species_by_name(pokemon)
          embed1=discord.Embed(title=pokemon, description=f"The pokémon spawned is {pokemon}\nNeed help? Join our [Support Server](https://discord.gg/YmVA2ah5tE)", color=0x2F3136)

          embed1.set_thumbnail(url=species.image_url)
        
          #await message.reply(embed=embed1, view=Confirm(message.content, pokemon, pokemon, self.bot))
          await message.reply(embed=embed1)
        
    
    #if message.author.id == 716390085896962058 and "The pokémon is" in message.content:
        #solution = hint_solve(message.content)
   
        #embed1=discord.Embed(title=solution[0].capitalize(), description=f"The pokémon spawned is {solution[0]}\nNeed help? Join our [Support Server](https://discord.gg/mhcjdJkxn6)", color=0x2F3136)
        #species = self.bot.data.species_by_name(solution[0])
        #embed1.set_thumbnail(url=species.image_url)
        #await message.channel.send(embed=embed1)
    
  
        
    if message.embeds and message.author.id == 716390085896962058:
      if "wild" in message.embeds[0].title:
        
        free = self.get_ratelimit(message)
        
        total_servers = config.basic_premium + config.premium + config.unlimited_premium
        val = (message.guild.id in total_servers)
        
        
        if val == False:
            if free is None:
                try:
                    await self.identify(message.embeds[0].image.url, message, "Free")
                except:
                    return
            else:
                return
            
        elif message.guild.id in config.unlimited_premium:
            try:
                await self.premium_identify(message.embeds[0].image.url, message, "Unlimited")
            except:
                return
            
        elif message.guild.id in config.unlimited_premium:
                try:
                    await self.premium_identify(message.embeds[0].image.url, message, "Unlimited")
                except:
                    return
        
        elif message.guild.id in config.basic_premium:
                try:
                    await self.premium_identify(message.embeds[0].image.url, message, "Basic")
                except:
                    return
            
        elif message.guild.id in config.premium:
                try:
                    await self.premium_identify(message.embeds[0].image.url, message, "Premium")
                except:
                    return
           
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
