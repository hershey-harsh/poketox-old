import discord
from discord.ext import commands, menus
import typing

class Dropdown(discord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Miscellaneous', description='View Pokétwo Miscellaneous commands', emoji='<:poketwo:964311966384554025>'),
            discord.SelectOption(label='Collectors', description='View collectors commands', emoji='<:pokeball:936773252913700894>'),
            discord.SelectOption(label='Shiny Hunt', description='View Shiny Hunt commands', emoji='✨'),
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Choose your favourite colour...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        await interaction.response.send_message(f'Your favourite colour is {self.values[0]}')


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown())
        
class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group(invoke_without_command=True, ignore_extra=False)
  async def help(self, ctx):
    await ctx.send("Hey", view=DropdownView())
    
def setup(bot):
    print("Loaded Help")
    bot.add_cog(Help(bot))
