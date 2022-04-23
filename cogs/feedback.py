import discord
from discord.ext import commands
from discord.ui import Modal, TextInput

# Defines a custom Modal with questions
# that user has to answer. The callback function
# of this class is called when the user submits the modal
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

        await interaction.response.send_message(
            f"Your name is {self.children[0].value}\n" f"The meaning of life is {self.children[1].value}\n"
        )


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
        
    @commands.command(brief="Suggest new features")
    async def feedback(self, ctx: commands.Context):
        """Sends a feedback form"""
    
        view = ModalView()
        await ctx.send("Click to open modal:", view=view)
      
def setup(bot):
    print("Loaded Feedback")
    bot.add_cog(feedbac(bot))