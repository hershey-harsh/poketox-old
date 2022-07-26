import discord
from name import identifyy
from discord.ext import commands
from discord import app_commands

class Confirm(discord.ui.View):
    def __init__(self, species, bot):
        super().__init__()
        self.species = species
        self.bot = bot
        
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

class predict_app(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        self.ctx_menu = app_commands.ContextMenu(
            name='Identify Pokémon',
            callback=self.app_identify,
        )
        
        self.bot.tree.add_command(self.ctx_menu)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)
        
    async def app_identify(self, interaction: discord.Interaction, message: discord.Message) -> None:
        if message.embeds:
            url = message.embeds[0].image.url
            
        else:
            url = message.content
        
        pokemon = await identifyy(url)
        species = self.bot.data.species_by_name(pokemon)
        
        if species is None:
          return await interaction.response.send_message(f"Could not find a pokemon matching `{pokemon}`.")
        
        embed=discord.Embed(title=f'{species}', description=f"This pokémon is **{species}**", color=0x2F3136)
        embed.set_thumbnail(url=species.image_url)
        
        await interaction.response.send_message(embed=embed, view=Confirm(pokemon, self.bot))
                                                
async def setup(bot):
    print("Loaded Predict App")
    await bot.add_cog(predict_app(bot))
