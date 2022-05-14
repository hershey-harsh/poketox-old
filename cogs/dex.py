import discord
from discord.ext import commands, menus
from helpers import checks
from helpers.converters import FetchUserConverter, SpeciesConverter
from discord.ext import commands, menus
from discord.ext import commands, tasks

class Confirm(discord.ui.View):
    def __init__(self, species, bot):
        super().__init__()
        self.value = None
        self.species = species
        self.bot = bot
        
    @discord.ui.button(label="Shiny Dex", style=discord.ButtonStyle.blurple, emoji="✨")
    async def info(self, interaction: discord.Interaction, button: discord.ui.Button):

        species = self.species
            
        shiny = True
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

        if shiny:
            embed.title = f"#{species.dex_number} — ✨ {species}"
            embed.set_thumbnail(url=species.shiny_image_url)
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

class dex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @checks.has_started()
    @commands.hybrid_command()
    async def dex(self, ctx, pokemon):
        """Show Pokédex info"""
        shiny = False

        if pokemon.isdigit():
            species = self.bot.data.species_by_number(int(pokemon))
        else:
            if pokemon.lower().startswith("shiny "):
                shiny = True
                species = species[6:]

            species = self.bot.data.species_by_name(pokemon)
            if species is None:
                return await ctx.send(f"Could not find a pokemon matching `{pokemon}`.")

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

        if shiny:
            embed.title = f"#{species.dex_number} — ✨ {species}"
            embed.set_thumbnail(url=species.shiny_image_url)
            view = None
        else:
            embed.set_thumbnail(url=species.image_url)
            view = Confirm(pokemon, self.bot)

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

        await ctx.send(embed=embed, view=view)
        
async def setup(bot):
  print("Loaded Dex")
  await bot.add_cog(dex(bot))
