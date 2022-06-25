import discord
from discord.ext import commands, menus
from discord.ext import commands, tasks
from helpers.converters import FetchUserConverter, SpeciesConverter
import random
import asyncio
import os
import datetime

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageDraw
import requests
from io import BytesIO

from replit import db
from cogs import collectors
import name
import config
import re
import string
from helpers import checks
from discord_webhook import DiscordWebhook, DiscordEmbed
import json
import requests

def make_name_embed(url, pokemon, description, filename):
  r = requests.get(url)
  im1 = Image.open('spawn_background.png')
  im2 = Image.open(BytesIO(r.content))
  
  if "alolan" in pokemon.lower():
    im1 = im1.resize((402, 112))

  if "hisuian" in pokemon.lower():
    im1 = im1.resize((402, 112))

  resized_image = im2.resize((100, 100))
  resized_image.save("new_test.png", quality=100, subsampling=0)

  back_im = im1.copy()

  if "alolan" in pokemon.lower():
    font = ImageFont.truetype("TitanOne-Regular.ttf", 25)
    back_im.paste(resized_image, (295, 5), mask=resized_image)

  elif "hisuian" in pokemon.lower():
    font = ImageFont.truetype("TitanOne-Regular.ttf", 25)
    back_im.paste(resized_image, (295, 5), mask=resized_image)

  else:
    back_im.paste(resized_image, (225, 5), mask=resized_image)
    font = ImageFont.truetype("TitanOne-Regular.ttf", 35)
  
  des_font = ImageFont.truetype("TitanOne-Regular.ttf", 11)

  draw = ImageDraw.Draw(back_im)
  draw.text((20, 10),pokemon,(255,255,255),font=font)
  draw.text((20, 50),description,(255,255,255),font=des_font)

  back_im.save(f'{filename}.png', quality=100, subsampling=0)
  return "Worked"

async def blocked_make_name_embed(url, pokemon, filename):
  print(pokemon)
  loop = asyncio.get_running_loop() 
  description = f'The pokémon spawned is {pokemon}'
  result = await loop.run_in_executor(None, make_name_embed, url, pokemon, description, filename)
  print(result)

no_spawn = [844392814485831710, 856328341702836265, 772557819303297054, 849169202966429696]

with open("pokemon.txt","r",encoding="utf8") as file:
    pokemon_list_string = file.read()
    
with open("rare.txt","r",encoding="utf8") as file:
    rare_pokes = file.read()

whitelist = [859326781927194674, 772937584884056135]
ad = ["Want to support the bot? Run `a!premium`", "Need help? Join our [server](https://discord.gg/YmVA2ah5tE)", "We have frequent giveaways! Join our [server](https://discord.gg/YmVA2ah5tE)", "Want the bot? Invite it [here](https://discord.com/oauth2/authorize?client_id=875526899386953779&scope=bot%20applications.commands&permissions=388168)"]
allowed = [826928105922232350, 826935014049972265, 797151240173125662, 875526899386953779]

q = ["Xen is made by Future#9409", "Like the bot? Type -invite in the bot's DM", "Want to help? DM Future#9409", "Join the offical server! https://discord.gg/futureworld"]

class Confirm(discord.ui.View):
    def __init__(self, species, bot):
        super().__init__()
        self.value = None
        self.species = species
        self.bot = bot

class Image_Text(discord.ui.View):
    def __init__(self, pokemon, image_url, bot):
        super().__init__()
        self.pokemon = pokemon
        self.image_url = image_url
        self.bot = bot

    @discord.ui.button(label='Text', style=discord.ButtonStyle.gray)
    async def tex(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        embed=discord.Embed(title=self.pokemon.capitalize(), description=f"The pokémon spawned is {self.pokemon.capitalize()}", color=0x303136)
        embed.set_thumbnail(url=self.image_url)
        
        await interaction.message.edit(content=None, attachment=None, embed=embed, view=Confirm(self.pokemon, self.bot))
        await interaction.response.send_message('Changed the message!', ephemeral=True)
        self.stop()
        
    @discord.ui.button(label="Dex Info", style=discord.ButtonStyle.gray)
    async def info(self, interaction: discord.Interaction, button: discord.ui.Button):

        species = self.pokemon
      
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
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Thanks for contributing to the bot! We reported the incorrect prediction to the Owner!", ephemeral=True)
        data = {"content" : f'Reported by: **{interaction.user.name}** *({interaction.user.id})*{self.url}',"username" : "Incorrect Prediction"}

        url = "https://discord.com/api/webhooks/936421747102744666/1UUkTqapNUlsYTZqKkR_s_EL4IwniPL4w9VKlL_QfMh8FV9zwpm0bkUkVsXA3est57T1"

        requests.post(url, json = data)
        self.value = True
        self.stop()

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
    self._free = commands.CooldownMapping.from_cooldown(1, 20.0, commands.BucketType.guild)

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
                
          if allow_mode == "Idk":
                pokemon = await name.identifyy(img_url)
                species = self.bot.data.species_by_name(pokemon)
                ctx = await self.bot.get_context(message)
                await collectors.shinyping(self, ctx, species)
                await collectors.collectping(self, ctx, species)
                
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
        
          #embed1=discord.Embed(title=species, description=f"The pokémon spawned is {species}\n{random.choice(ad)}", color=0x2F3136)
          
        
          #embed1=discord.Embed(title=species, description=f"The pokémon spawned is {species}", color=0x2F3136)
          #embed1.add_field(name="Giveaway", value="Pokétox is having a giveaway worth over 5,000,000 pokécoins. Type `a!giveaway` to learn more!", inline=False)
          #embed1.set_thumbnail(url=species.image_url)
          #embed1.set_footer(text=f'Server Plan: {plan}\nType a!update')
        
          filename = random.choice(string.ascii_letters)
          await blocked_make_name_embed(species.image_url, species.name, filename)
          await message.reply(file=discord.File(f'{filename}.png'), view=Image_Text(species.name, species.image_url, self.bot))
          os.remove(f'{filename}.png')
        
          #await message.reply(embed=embed1, view=Confirm(img_url, pokemon, pokemon, self.bot))
          #await message.reply(embed=embed1)

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
    if spawn_count >= 5000:
        return
    
    else:
    
          try:
                allow_mode = guild["name"]
          except: 
                allow_mode = "On"
                
          if allow_mode == "Idk":
                pokemon = await name.identifyy(img_url)
                species = self.bot.data.species_by_name(pokemon)
                ctx = await self.bot.get_context(message)
                await collectors.shinyping(self, ctx, species)
                await collectors.collectping(self, ctx, species)
                
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
        
          #embed1=discord.Embed(title=species, description=f"The pokémon spawned is {species}\n{random.choice(ad)}", color=0x2F3136)
          #embed1=discord.Embed(title=species, description=f"The pokémon spawned is {species}", color=0x2F3136)
          #embed1.add_field(name="Giveaway", value="Pokétox is having a giveaway worth over 5,000,000 pokécoins. Type `a!giveaway` to learn more!", inline=False)

          #embed1.set_thumbnail(url=species.image_url)
          #embed1.set_footer(text=f'Server Plan: {plan}\nType a!update')
        
          #await message.reply(embed=embed1, view=Confirm(img_url, pokemon, pokemon, self.bot))
          #await message.reply(embed=embed1)
          filename = random.choice(string.ascii_letters)
          print(filename)
          await blocked_make_name_embed(species.image_url, species.name, filename)
          print("Ran blocked code")
          await message.reply(file=discord.File(f'{filename}.png'), view=Image_Text(species.name, species.image_url, self.bot))
          print("Sent message")
          os.remove(f'{filename}.png')
          print("Removed image")
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
        
          print(str(total_count+1))
        
  @commands.has_permissions(manage_messages=True)            
  @commands.Cog.listener()
  async def on_message(self, message):
    
    if message.channel.id == 969956361616109578 and message.author.id != 875526899386953779:
          pokemon = await name.identifyy(img_url)
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
            if free == None:
                try:
                    await self.identify(message.embeds[0].image.url, message, "Free")
                except:
                    return
            else:
                try:
                    await message.add_reaction("⌛")
                    return
                except:
                    pass
                return
            
        elif message.guild.id in config.unlimited_premium:
                await self.premium_identify(message.embeds[0].image.url, message, "Unlimited")
            
        elif message.guild.id in config.unlimited_premium:
                await self.premium_identify(message.embeds[0].image.url, message, "Unlimited")
        
        elif message.guild.id in config.basic_premium:
                await self.premium_identify(message.embeds[0].image.url, message, "Basic")
            
        elif message.guild.id in config.premium:
                await self.premium_identify(message.embeds[0].image.url, message, "Premium")
           
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
