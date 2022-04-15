import discord
from discord.ext import commands, menus
import typing

class Dropdown(discord.ui.Select):
    def __init__(self, ctx):
        self.ctx = ctx

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Miscellaneous', description='View Pokétwo Miscellaneous commands', emoji='<:poketwo:964311966384554025>'),
            discord.SelectOption(label='Collectors', description='View Collectors commands', emoji='<:pokeball:936773252913700894>'),
            discord.SelectOption(label='Shiny Hunt', description='View Shiny Hunt commands', emoji='✨'),
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Choose the category', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        if self.values[0] == "Miscellaneous":
            embed=discord.Embed(title="Miscellaneous", description=f"You can do `{self.ctx.prefix}help <command>` to get more information about the command", color=0x2F3136)
            embed.add_field(name="Stats", value=f"`{self.ctx.prefix}stats <pokémon>`", inline=True)
            embed.add_field(name="Weakness", value=f"`{self.ctx.prefix}weakness <pokémon>`", inline=True)
            embed.add_field(name="Nature", value=f"`{self.ctx.prefix}nature <pokémon>`", inline=True)
            embed.add_field(name="Moveset", value=f"`{self.ctx.prefix}moveset <pokémon>`", inline=True)
            embed.add_field(name="Identify", value=f"`{self.ctx.prefix}identify <pokémon_url>`", inline=True)
            embed.add_field(name="Dex", value=f"`{self.ctx.prefix}dex <pokémon>`", inline=True)
            await interaction.response.send_message(embed=embed)
            
        if self.values[0] == "Shiny Hunt":
            embed=discord.Embed(title="Shiny Hunt", description=f"```diff\n- [] = optional argument\n- <> required argument\n+ Type {self.ctx.prefix}help [command | category]```")
            embed.add_field(name="Shinyhunt", value=f"`{self.ctx.prefix}shinyhunt <pokémon>`", inline=True)
            embed.add_field(name="Clear", value=f"`{self.ctx.prefix}shinyhunt clear`", inline=True)
            embed.add_field(name="View", value=f"`{self.ctx.prefix}shinyhunt view [user]`", inline=True)
            await interaction.response.send_message(embed=embed)


class DropdownView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

        # Adds the dropdown to our view object.
        self.add_item(Dropdown(self.ctx))
        
class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group(invoke_without_command=True, ignore_extra=False)
  async def help(self, ctx):
    await ctx.send("Hey", view=DropdownView(ctx))
    
def setup(bot):
    print("Loaded Help")
    bot.add_cog(Help(bot))
