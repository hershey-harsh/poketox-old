import discord
from discord.ext import commands, menus
from discord.ext import commands, tasks
from helpers.converters import FetchUserConverter, SpeciesConverter
import random
import asyncio
import os

from cogs import info

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageDraw
import requests
from io import BytesIO
from datetime import datetime
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

class Dropdown(discord.ui.Select):
    def __init__(self, ctx, pokemon_name, bot):
        self.ctx = ctx
        self.pokemon_name = pokemon_name
        self.bot = bot

        options = [
            discord.SelectOption(label='Dex Info', description=f'View dex info for {self.pokemon_name}'),
            discord.SelectOption(label='Nature', description=f'View nature for {self.pokemon_name}'),
            discord.SelectOption(label='Weakness', description=f'View weakness for {self.pokemon_name}'),
            discord.SelectOption(label='Names', description=f'View all names for {self.pokemon_name}'),
            discord.SelectOption(label='Statistics', description=f'View statistics for {self.pokemon_name}'),
            discord.SelectOption(label='Duel Statistics', description=f'View duelish statistics for {self.pokemon_name}'),
            discord.SelectOption(label='Moveset', description=f'View movesets for {self.pokemon_name}'),
            discord.SelectOption(label='Spawn Rate', description=f'View spawnrate for {self.pokemon_name}'),
        ]

        super().__init__(placeholder='Choose the category', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):

        if self.values[0] == "Dex Info":

          species = self.pokemon_name
      
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
      
        if self.values[0] == "Nature":
          try:
            reply = await info.get_nature_embed(self.pokemon_name)
          except:
            reply=discord.Embed(title=f"Data does not exist on {self.pokemon_name}", color=0x2f3136)
          await interaction.response.send_message(embed=reply,ephemeral=True)
            
        if self.values[0] == "Names":
          species = self.bot.data.species_by_name(self.pokemon_name)
          embed=discord.Embed(title=f"Names for {self.pokemon_name}", description="\n".join(f"{x} {y}" for x, y in species.names), color=0x2f3136)
          await interaction.response.send_message(embed=embed,ephemeral=True)
          
            
        if self.values[0] == "Statistics":
          species = self.bot.data.species_by_name(self.pokemon_name)

          base_stats = (
            f"**HP:** {species.base_stats.hp}",
            f"**Attack:** {species.base_stats.atk}",
            f"**Defense:** {species.base_stats.defn}",
            f"**Sp. Atk:** {species.base_stats.satk}",
            f"**Sp. Def:** {species.base_stats.sdef}",
            f"**Speed:** {species.base_stats.spd}",
          )
            
            
        if self.values[0] == "Duel Statistics":
          try:
            reply = await info.get_stats_embed(self.pokemon_name)
          except:
            reply=discord.Embed(title=f"Data does not exist on {self.pokemon_name}", color=0x2f3136)
          await interaction.response.send_message(embed=reply,ephemeral=True)
            
        if self.values[0] == "Moveset":
          try:
            reply = await info.get_moveset_embed(self.pokemon_name)
          except:
            reply=discord.Embed(title=f"Data does not exist on {self.pokemon_name}", color=0x2f3136)
          await interaction.response.send_message(embed=reply,ephemeral=True)
          
        print("Ran " + self.values[0])
            
        if self.values[0] == "Weakness":
          return
          
        if self.values[0] == "Spawn Rate":
          return
            

class DropdownView(discord.ui.View):
    def __init__(self, ctx, pokemon_name, bot):
        super().__init__()
        self.ctx = ctx
        self.pokemon_name = pokemon_name
        self.bot = bot

        # Adds the dropdown to our view object.
        self.add_item(Dropdown(self.ctx, self.pokemon_name, self.bot))

test = """
def make_name_embed(url, pokemon, filename):
  r = requests.get(url)
  im1 = Image.open('spawn_background.png')
  im2 = Image.open(BytesIO(r.content))
  
  im1 = im1.resize((312, 92))

  if "alolan" in pokemon.lower():
    im1 = im1.resize((402, 92))

  if "hisuian" in pokemon.lower():
    im1 = im1.resize((402, 92))

  resized_image = im2.resize((75, 75))
  resized_image.save("new_test.png", quality=100, subsampling=0)

  back_im = im1.copy()

  if "alolan" in pokemon.lower():
    font = ImageFont.truetype("TitanOne-Regular.ttf", 25)
    back_im.paste(resized_image, (300, 15), mask=resized_image)

  elif "hisuian" in pokemon.lower():
    font = ImageFont.truetype("TitanOne-Regular.ttf", 25)
    back_im.paste(resized_image, (300, 15), mask=resized_image)

  else:
    back_im.paste(resized_image, (225, 9), mask=resized_image)
    font = ImageFont.truetype("TitanOne-Regular.ttf", 35)
  
  des_font = ImageFont.truetype("TitanOne-Regular.ttf", 12)

  draw = ImageDraw.Draw(back_im)
  draw.text((13, 25),pokemon,(255,255,255),font=font)

  back_im.save(f'{filename}.png', quality=100, subsampling=0)
  return "Hi"
"""

from pilmoji import Pilmoji
from functools import reduce

repls = (':flag_jp:', '<:flag_jp:993180168304734338>'), (':flag_gb:', '<:flag_gb:993180161518354452>'), (':flag_de:', '<:flag_de:993180164626321439>'), (':flag_fr:', '<:flag_fr:993180166694117436>')

def make_name_embed(bot, url, pokemon, filename, desc=None):

  r = requests.get(url)
  im1 = Image.open('spawn_background.png')
  im2 = Image.open(BytesIO(r.content))
  
  im1 = im1.resize((312, 92))

  if "alolan" in pokemon.lower():
    im1 = im1.resize((402, 112))

  if "hisuian" in pokemon.lower():
    im1 = im1.resize((402, 112))

  resized_image = im2.resize((75, 75))
  resized_image.save("new_test.png", quality=100, subsampling=0)

  back_im = im1.copy()

  if "alolan" in pokemon.lower():
    font = ImageFont.truetype("TitanOne-Regular.ttf", 25)
    back_im.paste(resized_image, (300, 15), mask=resized_image)

  elif "hisuian" in pokemon.lower():
    font = ImageFont.truetype("TitanOne-Regular.ttf", 25)
    back_im.paste(resized_image, (300, 15), mask=resized_image)

  else:
    back_im.paste(resized_image, (229, 9), mask=resized_image)
    font = ImageFont.truetype("TitanOne-Regular.ttf", 35)
  
  des_font = ImageFont.truetype("TitanOne-Regular.ttf", 20)


  if desc is not None:
    
    pokemon_alt = []
    species = bot.data.species_by_name(pokemon)
    for x, y in species.names:
      pokemon_alt.append(f'{x} {y}')
    pokemon_alt.sort(key=len)
    
    try:
      if pokemon != pokemon_alt[1]:
        desc = reduce(lambda a, kv: a.replace(*kv), repls, pokemon_alt[1])
        with Pilmoji(back_im) as pilmoji:
          pilmoji.text((15, 53), desc,(255,255,255),font=des_font, emoji_position_offset=(0, 3))
        name_size_1 = 15
        name_size_2 = 15
    except:
        name_size_1 = 15
        name_size_2 = 25
        pass
  
  draw = ImageDraw.Draw(back_im)
  draw.text((name_size_1, name_size_2),pokemon,(255,255,255),font=font)
      
  back_im.save(f'{filename}.png', quality=100, subsampling=0)
  return "Hi"

async def blocked_make_name_embed(bot, url, pokemon, filename):
  loop = asyncio.get_running_loop()
  
  result = await loop.run_in_executor(None, make_name_embed, bot, url, pokemon, filename, "Test")

no_spawn = [844392814485831710, 856328341702836265, 772557819303297054, 849169202966429696]

hisuian = ["Hisuian Growlithe", "Hisuian Arcanine", "Hisuian Voltorb", "Hisuian Electrode", "Hisuian Typhlosion", "Hisuian Qwilfish", "Hisuian Sneasel", "Hisuian Samurott", "Hisuian Lilligant", "Hisuian Zorua", "Hisuian Zoroark", "Hisuian Braviary", "Hisuian Sliggoo", "Hisuian Goodra", "Hisuian Avalugg", "Hisuian Decidueye", "Sneasler", "Overqwil", "Wyrdeer", "Ursaluna"]
alolan = ["Alolan Rattata", "Alolan Raticate", "Alolan Raichu", "Alolan Sandshrew", "Alolan Sandslash", "Alolan Vulpix", "Alolan Ninetales", "Alolan Diglett", "Alolan Dugtrio", "Alolan Meowth", "Alolan Persian", "Alolan Geodude", "Alolan Graveler", "Alolan Golem", "Alolan Grimer", "Alolan Muk", "Alolan Exeggutor", "Alolan Marowak"]
galarian = ["Galarian Zigzagoon", "Galarian Linoone", "Obstagoon", "Galarian Meowth", "Perrserker", "Galarian Ponyta", "Galarian Rapidash", "Galarian Slowpoke", "Galarian Slowbro", "Galarian Slowking", "Galarian Corsola", "Cursola", "Galarian Farfetch’d", "Sirfetch'd", "Galarian Weezing", "Galarian Mr. Mime", "Mr. Rime", "Galarian Darumaka", "Galarian Darmanitan", "Galarian Yamask", "Runerigus", "Galarian Stunfisk", "Galarian Articuno", "Galarian Zapdos", "Galarian Moltres"]

with open("pokemon.txt","r",encoding="utf8") as file:
    pokemon_list_string = file.read()

f = open('rare.txt', 'r')
file = f.read()
file = file.split('\n')

rare_pokes = []
for i in file:
    if len(i) >= 3:
        rare_pokes.append(i)
    
total_rare_pokes = hisuian+alolan+galarian+rare_pokes

whitelist = [859326781927194674, 772937584884056135]
ad = ["Want to support the bot? Run `a!premium`", "Need help? Join our [server](https://discord.gg/YmVA2ah5tE)", "We have frequent giveaways! Join our [server](https://discord.gg/YmVA2ah5tE)", "Want the bot? Invite it [here](https://discord.com/oauth2/authorize?client_id=875526899386953779&scope=bot%20applications.commands&permissions=388168)"]
allowed = [826928105922232350, 826935014049972265, 797151240173125662, 875526899386953779]
allowed = [950522564751544330, 716390085896962058]

q = ["Xen is made by Future#9409", "Like the bot? Type -invite in the bot's DM", "Want to help? DM Future#9409", "Join the offical server! https://discord.gg/futureworld"]

class Jump(discord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        url = query

        # Link buttons cannot be made with the decorator
        # Therefore we have to manually create one.
        # We add the quoted url to the button, and add the button to the view.
        self.add_item(discord.ui.Button(label='Go to original message', url=url))

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
        
        await interaction.message.edit(content=None, attachments=[], embed=embed, view=Confirm(self.pokemon, self.bot))
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
    self._free = commands.CooldownMapping.from_cooldown(1, 10.0, commands.BucketType.guild)

  def get_ratelimit(self, message):
        bucket = self._free.get_bucket(message)
        return bucket.update_rate_limit()
    
  async def premium_identify(self, img_url, message, plan):
    timest = discord.utils.format_dt(datetime.now(), 'R')
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
        
          pokemon = await name.identifyy(img_url)
      
          species = self.bot.data.species_by_name(pokemon)
        
          #embed1=discord.Embed(title=species, description=f"The pokémon spawned is {species}\n{random.choice(ad)}", color=0x2F3136)
          
        
          #embed1=discord.Embed(title=species, description=f"The pokémon spawned is {species}", color=0x2F3136)
          #embed1.add_field(name="Giveaway", value="Pokétox is having a giveaway worth over 5,000,000 pokécoins. Type `a!giveaway` to learn more!", inline=False)
          #embed1.set_thumbnail(url=species.image_url)
          #embed1.set_footer(text=f'Server Plan: {plan}\nType a!update')
          
          if allow_mode == "On":
            filename = random.choice(string.ascii_letters)
            await blocked_make_name_embed(self.bot, species.image_url, species.name, filename)
            await message.reply(file=discord.File(f'{filename}.png'), view=DropdownView(ctx, species.name, self.bot))
            os.remove(f'{filename}.png')
        
          #await message.reply(embed=embed1, view=Confirm(img_url, pokemon, pokemon, self.bot))
          #await message.reply(embed=embed1)
                        
          ctx = await self.bot.get_context(message)
          guild = await ctx.bot.mongo.fetch_guild(ctx.guild)
                
          try:
            await collectors.shinyping(self, ctx, species)
            await collectors.collectping(self, ctx, species)
          except:
                pass
            
          try:
            
            if guild['specialized'] and ctx.channel.id not in guild['specialized']:
                return
            
            if pokemon.title() in rare_pokes:
                try:
                    roleid = guild["rareping"]
                    await message.channel.send(f'**Specialized Ping**\n<@&{roleid}>')
                except:
                    pass
                
            elif pokemon in hisuian:
                try:
                    roleid = guild["alolanping"]
                    await message.channel.send(f'**Specialized Ping**\n<@&{roleid}>')
                except:
                    pass
                
            elif pokemon in alolan:
                try:
                    roleid = guild["galarianping"]
                    await message.channel.send(f'**Specialized Ping**\n<@&{roleid}>')
                except:
                    pass
                
            elif pokemon in galarian:
                try:
                    roleid = guild["hisuianping"]
                    await message.channel.send(f'**Specialized Ping**\n<@&{roleid}>')
                except:
                    pass
                
          except:
            pass
 
          try:
            if pokemon.title() in total_rare_pokes:
                star_channel = self.bot.get_channel(int(guild["starboard"]))
                embed=discord.Embed(title=f"A wild {species.name} has appeared!", description=f"{species.lower} was spawned in {message.channel.id} {timest}", color=0x2f3136)
                embed.set_thumbnail(url=species.image_url)
                await star_channel.send(embed=embed, view=Jump(plan))
          except:
            pass
    
  async def identify(self, img_url, message, plan):
    ctx = await self.bot.get_context(message)
    timest = discord.utils.format_dt(datetime.now(), 'R')
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
        
          pokemon = await name.identifyy(img_url)
      
          species = self.bot.data.species_by_name(pokemon)
        
          #embed1=discord.Embed(title=species, description=f"The pokémon spawned is {species}\n{random.choice(ad)}", color=0x2F3136)
          #embed1=discord.Embed(title=species, description=f"The pokémon spawned is {species}", color=0x2F3136)
          #embed1.add_field(name="Giveaway", value="Pokétox is having a giveaway worth over 5,000,000 pokécoins. Type `a!giveaway` to learn more!", inline=False)

          #embed1.set_thumbnail(url=species.image_url)
          #embed1.set_footer(text=f'Server Plan: {plan}\nType a!update')
        
          #await message.reply(embed=embed1, view=Confirm(img_url, pokemon, pokemon, self.bot))
          #await message.reply(embed=embed1)
        
          if allow_mode == "On":
            filename = random.choice(string.ascii_letters)
            await blocked_make_name_embed(self.bot, species.image_url, species.name, filename)
            await message.reply(file=discord.File(f'{filename}.png'), view=DropdownView(ctx, species.name, self.bot))
            os.remove(f'{filename}.png')
                
          try:
                await collectors.shinyping(self, ctx, species)
                await collectors.collectping(self, ctx, species)
          except:
                pass
        
          try:
            
            if guild['specialized'] and ctx.channel.id not in guild['specialized']:
                return
            
            if pokemon.title() not in total_rare_pokes:
                return
            
            if pokemon in rare_pokes:
                try:
                    roleid = guild["rareping"]
                    await message.channel.send(f'**Specialized Ping**\n<@&{roleid}>')
                except:
                    pass
                
            elif pokemon in hisuian:
                try:
                    roleid = guild["alolanping"]
                    await message.channel.send(f'**Specialized Ping**\n<@&{roleid}>')
                except:
                    pass
                
            elif pokemon in alolan:
                try:
                    roleid = guild["galarianping"]
                    await message.channel.send(f'**Specialized Ping**\n<@&{roleid}>')
                except:
                    pass
                
            elif pokemon in galarian:
                try:
                    roleid = guild["hisuianping"]
                    await message.channel.send(f'**Specialized Ping**\n<@&{roleid}>')
                except:
                    pass
                
          except:
            pass
        
          try:
            if pokemon.title() in total_rare_pokes:
                star_channel = self.bot.get_channel(int(guild["starboard"]))
                embed=discord.Embed(title=f"A wild {species.name} has appeared!", description=f"{species.lower} was spawned in {message.channel.id} {timest}", color=0x2f3136)
                embed.set_thumbnail(url=species.image_url)
                await star_channel.send(embed=embed, view=Jump(plan))
          except:
            pass
        
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
    
  
    
    if message.embeds and message.author.id in allowed:
      if "wild" in message.embeds[0].title:
        
        free = self.get_ratelimit(message)
        
        total_servers = config.basic_premium + config.premium + config.unlimited_premium
        val = (message.guild.id in total_servers)
        
        
        if val == False:
            if free == None:
                    await self.identify(message.embeds[0].image.url, message, message.jump_url)
            else:
                try:
                    await message.add_reaction("⌛")
                    return
                except:
                    pass
                return
            
        elif message.guild.id in config.unlimited_premium:
                await self.premium_identify(message.embeds[0].image.url, message, message.jump_url)
            
        elif message.guild.id in config.unlimited_premium:
                await self.premium_identify(message.embeds[0].image.url, message, message.jump_url)
        
        elif message.guild.id in config.basic_premium:
                await self.premium_identify(message.embeds[0].image.url, message, message.jump_url)
            
        elif message.guild.id in config.premium:
                await self.premium_identify(message.embeds[0].image.url, message, message.jump_url)
           
async def setup(bot):
    print("Loaded Pokedex")
    await bot.add_cog(Pokedex(bot))
