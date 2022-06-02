import discord
from discord.ext import commands
import random
import time
import config
from helpers import checks
import asyncio
import requests
import json
import asyncio
import datetime
from name import solve
import name

class Confirm(discord.ui.View):
    def __init__(self, url, species, bot):
        super().__init__()
        self.value = None
        self.url = url
        self.species = species
        self.bot = bot

        url = f"https://discord.com/oauth2/authorize?client_id=875526899386953779&scope=bot%20applications.commands&permissions=388168"

        self.add_item(discord.ui.Button(label="Bot Invite", url=url))

        url = "https://discord.gg/YmVA2ah5tE"

        self.add_item(discord.ui.Button(label="Support Server", url=str(url)))
        
    @discord.ui.button(label="Dex Info", style=discord.ButtonStyle.gray)
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

    @discord.ui.button(label="Incorrect Prediction", style=discord.ButtonStyle.gray)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Thanks for contributing to the bot! We reported the incorrect prediction to the Owner!", ephemeral=True)
        data = {"content" : f'Reported by: **{interaction.user.name}** *({interaction.user.id})*{self.url}',"username" : "Incorrect Prediction"}

        url = "https://discord.com/api/webhooks/936421747102744666/1UUkTqapNUlsYTZqKkR_s_EL4IwniPL4w9VKlL_QfMh8FV9zwpm0bkUkVsXA3est57T1"

        requests.post(url, json = data)
        self.value = True
        self.stop()

class identifyy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.has_started()
    @commands.command()
    async def identify(self, ctx, *, url):
          pokemon = await name.identifyy(url)
      
          species = pokemon
            
          species = self.bot.data.species_by_name(species)
        
          if species is None:
            return await ctx.send(f"Could not find a pokemon matching `{species}`.")
          embed1=discord.Embed(title=f'{species}',color=0x2F3136)

          if species.description:
              embed1.add_field(name="Description",value= species.description.replace("\n", " "),inline=False)

          embed1.set_image(url=url)
          embed1.set_thumbnail(url=species.image_url)

          await ctx.reply(embed=embed1, view=Confirm(url, pokemon, self.bot), mention_author=False)

async def setup(bot):
    print("Loaded Identify")
    await bot.add_cog(identifyy(bot))
