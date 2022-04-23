import discord
from discord.ext import commands
from discord.ui import Modal, TextInput
from discord.ext import commands, menus
import typing

# Defines a custom Modal with questions
# that user has to answer. The callback function
# of this class is called when the user submits the modal

class Dropdown(discord.ui.Select):
    def __init__(self, ctx):
        self.ctx = ctx

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Spawn Identifying', description='Why our spawn identifying is better?', emoji='<:pokeball:936773252913700894>'),
            discord.SelectOption(label='Automatic Pings', description='Why our Automatic Pings are better?', emoji='✨'),
            discord.SelectOption(label='Miscellaneous', description='Why our miscellaneous commands are better?', emoji='<:poketwo:964311966384554025>'),
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Choose the category', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):

        if self.values[0] == "Spawn Identifying":
            embed=discord.Embed(title="ℹ️ Why should you use Pokétox?", description="Poketwo reimagined — Assists you with catching, price checks pokémons, automatically pings Shiny Hunters, and much more. Overall Pokétox provides the best User Interface.", color=0x2F3136)
            embed.add_field(name="Spawn Identifying", value="Although other bots have this feature — Pokétox makes its much better because it doesn't send a low quality image with the pokémon name in it, rather it sends the pokémons name in the title and provides a button which when you click gives you all the dex information.", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        if self.values[0] == "Automatic Pings":
            embed=discord.Embed(title="ℹ️ Why should you use Pokétox?", description="Poketwo reimagined — Assists you with catching, price checks pokémons, automatically pings Shiny Hunters, and much more. Overall Pokétox provides the best User Interface.", color=0x2F3136)
            embed.add_field(name="Automatic Pings", value="There are no bots out there that ping you for Collecting Lists — Only few bots automatically ping you for Shiny Hunts including Pokétox. You can also add regions to your collecting lists instead of individual pokémons.", inline=True)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        if self.values[0] == "Miscellaneous":
            embed=discord.Embed(title="ℹ️ Why should you use Pokétox?", description="Poketwo reimagined — Assists you with catching, price checks pokémons, automatically pings Shiny Hunters, and much more. Overall Pokétox provides the best User Interface.", color=0x2F3136)
            embed.add_field(name="Miscellaneous", value="There are some bots out there that provide Shiny Rate, and Spawn Rate and so on... Meanwhile Pokétox provides all those features including Duel Stats, Weakness, Nature, Moveset, Dex, Spawn Rate, and Price Check commands which no other bot provides. These commands are unique to Pokétox.", inline=True)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)

class DropdownView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

        # Adds the dropdown to our view object.
        self.add_item(Dropdown(self.ctx))

class MyModal(Modal):
    def __init__(self) -> None:
        super().__init__("Pokétox Feedback")
        
        self.add_item(
            TextInput(
                label="What is your most favorite about Pokétox?",
                placeholder="Identify Spawns, Automatic Pings, Price Check",
                style=discord.TextInputStyle.long,
            )
        )
        
        self.add_item(
            TextInput(
                label="What is your least favorite about Pokétox?",
                placeholder="Identify Spawns, Automatic Pings, Price Check",
                style=discord.TextInputStyle.long,
            )
        )
        
        self.add_item(
            TextInput(
                label="What features do you want to see in Pokétox?",
                placeholder="Commands that don't exist yet",
                style=discord.TextInputStyle.long,
            )
        )
        
        self.add_item(
            TextInput(
                label="Would you use Pokétox over other naming bots?",
                placeholder="I would use because / I would not use because",
                style=discord.TextInputStyle.long,
            )
        )
        
        self.add_item(
            TextInput(
                label="Do other bots provide better features?",
                placeholder="Yes because / No because",
                style=discord.TextInputStyle.long,
            )
        )
        
    async def callback(self, interaction: discord.Interaction):

        await interaction.response.send_message("Your feedback has been submitted. Thank you.")


class ModalView(discord.ui.View):
    @discord.ui.button(label="Open Survey", style=discord.ButtonStyle.primary)
    async def open_modal(self, button: discord.Button, interaction: discord.Interaction):
        # Create the modal
        modal = MyModal()

        # Sending a message containing our modal
        await interaction.response.send_modal(modal)
        
class feedbac(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group(invoke_without_command=True, ignore_extra=False, brief="Shows the help page")
    async def about(self, ctx):
        embed=discord.Embed(title="ℹ️ Why should you use Pokétox?", description="Poketwo reimagined — Assists you with catching, price checks pokémons, automatically pings Shiny Hunters, and much more. Overall Pokétox provides the best User Interface.", color=0x2F3136)
        await ctx.send(embed=embed, view=DropdownView(ctx))
        
        
    @commands.command(brief="Suggest new features")
    async def feedback(self, ctx: commands.Context):
        """Sends a feedback form"""
        embed=discord.Embed(title="Feedback", description="Please click the button below to start the feedback form. Please keep in mind to include any negative feedbacks as well as positive feedbacks since we want to hear from everyone including people that don't like the bot", color=0x2F3136)
        view = ModalView()
        await ctx.send(embed=embed, view=view)
      
def setup(bot):
    print("Loaded Feedback")
    bot.add_cog(feedbac(bot))
