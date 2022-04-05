import discord
from discord.ext import commands
import random
import time
import config

import asyncio
import requests
import json

class Confirm(discord.ui.View):
    def __init__(self, url):
        super().__init__()
        self.value = None
        self.url = url

        url = f"https://discord.com/oauth2/authorize?client_id=875526899386953779&scope=bot%20applications.commands&permissions=388168"

        self.add_item(discord.ui.Button(label="Bot Invite", url=url))

        url = "https://discord.gg/mhcjdJkxn6"

        self.add_item(discord.ui.Button(label="Support Server", url=str(url)))

    @discord.ui.button(label="Incorrect Prediction", style=discord.ButtonStyle.gray)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Thanks for contributing to the bot! We reported the incorrect prediction to the Owner!", ephemeral=True)
        data = {"content" : f'Reported by: **{interaction.user.name}** *({interaction.user.id})*{self.url}',"username" : "Incorrect Prediction"}

        url = "https://discord.com/api/webhooks/936421747102744666/1UUkTqapNUlsYTZqKkR_s_EL4IwniPL4w9VKlL_QfMh8FV9zwpm0bkUkVsXA3est57T1"

        requests.post(url, json = data)
        self.value = True
        self.stop()

def solve(url):
  try:
    response = requests.get(url)
    file = open("pokemon.png", "wb")
    file.write(response.content)
    file.close()

    with open('pokemon.png', 'rb') as f:
      img = f.read()
    
    r2 = requests.post('https://api-inference.huggingface.co/models/imjeffhi/pokemon_classifier', data=img)

    pokemon = r2.json()
    return pokemon[0]['label']

  except:
    try:
      endpoint = 'https://main-pokemon-classifier-imjeffhi4.endpoint.ainize.ai/classify/'
      r3 = requests.post(endpoint, json={"poke_image": url})
      result = r3.json()
      return result['Name']
    except:
      myobj = {'file': open('pokemon.png', 'rb')}
      x = requests.post("https://pokemon-classifier.herokuapp.com/analyze", files=myobj)
      pokem = x.json()
      return pokem['result']

class identify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def identify(self, ctx, *, url):
          embed=discord.Embed(title="<a:loading:875500054868291585> Predicting...", color=0x2f3136)  
          pokemon = pokemon_name(url)

          aaa = await ctx.reply(embed=embed, view=Confirm(url), mention_author=False)
      
          species = pokemon
          embed1=discord.Embed(title=pokemon,color=0x2F3136)

          await aaa.edit(embed=embed1)

          species = self.bot.data.species_by_name(species)
        
          if species is None:
            return await ctx.send(f"Could not find a pokemon matching `{species}`.")
          embed1=discord.Embed(title=f'{pokemon}',color=0x2F3136)

          if species.description:
              embed1.add_field(name="Description",value= species.description.replace("\n", " "),inline=False)

          embed1.set_image(url=url)
          embed1.set_thumbnail(url=species.image_url)

          await aaa.edit(embed=embed1)

def setup(bot):
    print("Loaded Identify")
    bot.add_cog(identify(bot))
