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
        
    @discord.ui.button(label="Shiny", style=discord.ButtonStyle.blurple, emoji="✨")
    async def info(self, interaction: discord.Interaction, button: discord.ui.Button):

        species = self.species
      
        if species.isdigit():
            species = self.bot.data.species_by_number(int(species))
        else:
            
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
