import discord
from discord.ext import commands, menus
import typing

class Dropdown(discord.ui.Select):
    def __init__(self, ctx):
        self.ctx = ctx

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label='Miscellaneous', description='View Pokétwo Miscellaneous commands', emoji='<:poketwo:964311966384554025>'),
            discord.SelectOption(label='Fun', description='View Fun commands', emoji='🥳'),
            discord.SelectOption(label='Whitelist', description='View whitelist commands', emoji='✅')
            discord.SelectOption(label='Settings', description='Customize settings', emoji='⚙️'),
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
        if self.values[0] == "Settings":
            embed=discord.Embed(title="Settings", description=f"```diff\n- [] = optional argument\n- <> required argument\n+ Type {self.ctx.prefix}help [command | category]```", color=0x2F3136)
            embed.add_field(name="Enable", value=f"`{self.ctx.prefix}enable <setting>`", inline=True)
            embed.add_field(name="Disable", value=f"`{self.ctx.prefix}disable <setting>`", inline=True)
            embed.add_field(name="Toggle", value=f"`{self.ctx.prefix}toggle <setting>`", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        if self.values[0] == "Whitelist":
            embed=discord.Embed(title="Whitelist", description=f"```diff\n- [] = optional argument\n- <> required argument\n+ Type {self.ctx.prefix}help [command | category]```", color=0x2F3136)
            embed.add_field(name="Reset", value=f"`{self.ctx.prefix}whitelist reset`", inline=True)
            embed.add_field(name="All", value=f"`{self.ctx.prefix}whitelist all`", inline=True)
            embed.add_field(name="Shiny", value=f"`{self.ctx.prefix}whitelist shiny <channels>`", inline=True)
            embed.add_field(name="Collect", value=f"`{self.ctx.prefix}whitelist collect <channels>`", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        if self.values[0] == "Miscellaneous":
            embed=discord.Embed(title="Miscellaneous", description=f"```diff\n- [] = optional argument\n- <> required argument\n+ Type {self.ctx.prefix}help [command | category]```", color=0x2F3136)
            embed.add_field(name="Stats", value=f"`{self.ctx.prefix}stats <pokémon>`", inline=True)
            embed.add_field(name="Weakness", value=f"`{self.ctx.prefix}weakness <pokémon>`", inline=True)
            embed.add_field(name="Nature", value=f"`{self.ctx.prefix}nature <pokémon>`", inline=True)
            embed.add_field(name="Moveset", value=f"`{self.ctx.prefix}moveset <pokémon>`", inline=True)
            embed.add_field(name="Identify", value=f"`{self.ctx.prefix}identify <pokémon_url>`", inline=True)
            embed.add_field(name="Dex", value=f"`{self.ctx.prefix}dex <pokémon>`", inline=True)
            embed.add_field(name="Price", value=f"`{self.ctx.prefix}price <pokémon>`", inline=True)
            embed.add_field(name="Spawn Rate", value=f"`{self.ctx.prefix}spawnrate <pokémon>`", inline=True)
            embed.add_field(name="Shiny Rate", value=f"`{self.ctx.prefix}shinyrate <pokémon>`", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        if self.values[0] == "Fun":
            embed=discord.Embed(title="Fun", description=f"```diff\n- [] = optional argument\n- <> required argument\n+ Type {self.ctx.prefix}help [command | category]```", color=0x2F3136)
            embed.add_field(name="Who's that pokémon?", value=f"`{self.ctx.prefix}whosthatpokemon`", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        if self.values[0] == "Shiny Hunt":
            embed=discord.Embed(title="Shiny Hunt", description=f"```diff\n- [] = optional argument\n- <> required argument\n+ Type {self.ctx.prefix}help [command | category]```", color=0x2F3136)
            embed.add_field(name="Shinyhunt", value=f"`{self.ctx.prefix}shinyhunt <pokémon>`", inline=True)
            embed.add_field(name="Clear", value=f"`{self.ctx.prefix}shinyhunt clear`", inline=True)
            embed.add_field(name="View", value=f"`{self.ctx.prefix}shinyhunt view [user]`", inline=True)
            embed.set_footer(text=f"Must run {self.ctx.prefix}pings enable [serverid] to get pinged")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        if self.values[0] == "Collectors":
            embed=discord.Embed(title="Collecting", description=f"```diff\n- [] = optional argument\n- <> required argument\n+ Type {self.ctx.prefix}help [command | category]```", color=0x2F3136)
            embed.add_field(name="Collect", value=f"`{self.ctx.prefix}collectlist add <pokémon>`", inline=True)
            embed.add_field(name="Clear", value=f"`{self.ctx.prefix}collectlist clear`", inline=True)
            embed.add_field(name="Remove", value=f"`{self.ctx.prefix}collectlist remove <pokémon>`", inline=True)
            embed.add_field(name="View", value=f"`{self.ctx.prefix}collectlist view [user]`", inline=True)
            embed.set_footer(text=f"Must run {self.ctx.prefix}pings enable [serverid] to get pinged")
            await interaction.response.send_message(embed=embed, ephemeral=True)

class DropdownView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

        # Adds the dropdown to our view object.
        self.add_item(Dropdown(self.ctx))
        
class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  async def stats(self, ctx):
    embed=discord.Embed(title="Stats", color=0x36393F)
    embed.add_field(name="Usage & Description", value=f"Shows statistics needed for an duelish pokémon\n```\n{ctx.prefix}stats <pokémon>```", inline=False)
    await ctx.send(embed=embed)
    
  async def weakness(self, ctx):
    embed=discord.Embed(title="Weakness", color=0x36393F)
    embed.add_field(name="Usage & Description", value=f"Shows weakness for a pokémo\n```\n{ctx.prefix}weakness <pokémon>```", inline=False)
    await ctx.send(embed=embed)
    
  async def nature(self, ctx):
    embed=discord.Embed(title="Nature", color=0x36393F)
    embed.add_field(name="Usage & Description", value=f"Shows nature for a pokémon\n```\n{ctx.prefix}nature <pokémon>```", inline=False)
    await ctx.send(embed=embed)
    
  async def moveset(self, ctx):
    embed=discord.Embed(title="Moveset", color=0x36393F)
    embed.add_field(name="Usage & Description", value=f"Shows moves for a pokémo\n```\n{ctx.prefix}moveset <pokémon>```", inline=False)
    await ctx.send(embed=embed)
    
  async def identify(self, ctx):
    embed=discord.Embed(title="Identify", color=0x36393F)
    embed.add_field(name="Usage & Description", value=f"Shows the pokémon name using an image\n```\n{ctx.prefix}identify <pokémon>```", inline=False)
    await ctx.send(embed=embed)

  async def dex(self, ctx):
    embed=discord.Embed(title="Moveset", color=0x36393F)
    embed.add_field(name="Usage & Description", value=f"Shows pokédex information\n```\n{ctx.prefix}dex <pokémon>```", inline=False)
    await ctx.send(embed=embed)
    
  async def collectlist(self, ctx):
    embed=discord.Embed(title="Collect List", color=0x36393F)
    embed.add_field(name="Alias", value=f"{ctx.prefix}cl", inline=False)
    embed.add_field(name="Usage & Description", value=f"Adds a pokémon to your collecting list\n```\n{ctx.prefix}collectlist add <pokémon>```", inline=False)
    embed.add_field(name="Usage & Description", value=f"Clear your collecting list\n```\n{ctx.prefix}collectlist clear```", inline=False)
    embed.add_field(name="Usage & Description", value=f"Removes a pokémon from your collecting list\n```\n{ctx.prefix}collectlist remove <pokémon>```", inline=False)
    embed.add_field(name="Usage & Description", value=f"Allows members to view their collecting list\n```\n{ctx.prefix}collectlist view [member]```", inline=False)
    embed.add_field(name="Usage & Description", value=f"Lists the collectors of pokémon | 3 seconds cooldown\n```\n{ctx.prefix}collectlist globalsearch <pokémon>```", inline=False)
    embed.add_field(name="Usage & Description", value=f"Lists the collectors of pokémon in the server\n```\n{ctx.prefix}collectlist search <pokémon>```", inline=False)
    await ctx.send(embed=embed)
    
  async def shinyhunt(self, ctx):
    embed=discord.Embed(title="Shinyhunt", color=0x36393F)
    embed.add_field(name="Alias", value=f"{ctx.prefix}sh", inline=False)
    embed.add_field(name="Usage & Description", value=f"Add pokémon to shiny hunt\n```\n{ctx.prefix}shinyhunt <pokémon>```", inline=False)
    embed.add_field(name="Usage & Description", value=f"Clear your shiny hunt\n```\n{ctx.prefix}shinyhunt clear```", inline=False)
    embed.add_field(name="Usage & Description", value=f"Removes a pokémon from your collecting list\n```\n{ctx.prefix}shinyhunt view [user]```", inline=False)
    await ctx.send(embed=embed)
    
  async def price(self, ctx):
    embed=discord.Embed(title="Price Check", color=0x36393F)
    embed.add_field(name="Usage & Description", value=f"Shows estimated price about the pokémon\n```\n{ctx.prefix}price <pokémon>```", inline=False)
    await ctx.send(embed=embed)
    
  async def shinyrate(self, ctx):
    embed=discord.Embed(title="Shiny Rate", color=0x36393F)
    embed.add_field(name="Usage & Description", value=f"Shows shiny rate of a pokémon\n```\n{ctx.prefix}shinyrate <pokémon>```", inline=False)
    await ctx.send(embed=embed)
    
  async def toggle(self, ctx):
    embed=discord.Embed(title="Toggle", color=0x36393F)
    embed.add_field(name="Usage & Description", value=f"Toggles naming feature for server\n```\n{ctx.prefix}toggle naming```", inline=False)
    embed.add_field(name="Usage & Description", value=f"Toggles raredex feature for server\n```\n{ctx.prefix}toggle raredex setup <role>```", inline=False)
    await ctx.send(embed=embed)
    
  async def enable(self, ctx):
    embed=discord.Embed(title="Enable", color=0x36393F)
    embed.add_field(name="Usage & Description", value=f"Enable pings in a server\n```\n{ctx.prefix}enable pings [serverid] [collect] [shiny]```", inline=False)
    embed.add_field(name="Usage & Description", value=f"Enable catch logs in a server\n```\n{ctx.prefix}enable catchlogs [serverid]```", inline=False)
    await ctx.send(embed=embed)
    
  async def disable(self, ctx):
    embed=discord.Embed(title="Disable", color=0x36393F)
    embed.add_field(name="Usage & Description", value=f"Disable pings in a server\n```\n{ctx.prefix}disable pings [serverid] [collect] [shiny]```", inline=False)
    embed.add_field(name="Usage & Description", value=f"Disable catch logs in a server\n```\n{ctx.prefix}disable catchlogs [serverid]```", inline=False)
    await ctx.send(embed=embed)
    
  async def whitelist(self, ctx):
    embed=discord.Embed(title="Whitelist", color=0x36393F)
    embed.add_field(name="Usage & Description", value=f"Reset all channels for pings\n```\n{ctx.prefix}whitelist clear```", inline=False)
    embed.add_field(name="Usage & Description", value=f"Whitelist all channels for pings\n```\n{ctx.prefix}whitelist all```", inline=False)
    embed.add_field(name="Usage & Description", value=f"Whitelist shiny hunt in certain channels\n```\n{ctx.prefix}whitelist shiny <channels>```", inline=False)
    embed.add_field(name="Usage & Description", value=f"Whitelist collecting in certain channels\n```\n{ctx.prefix}toggle collect <channels>```", inline=False)
    
    await ctx.send(embed=embed)
    
  async def wtp(self, ctx):
    embed=discord.Embed(title="Who's that Pokémon", color=0x36393F)
    embed.add_field(name="Usage & Description", value=f'Sends a "Who\'s that Pokémon" image with answer\n```\n{ctx.prefix}whosthatpokemon clear```', inline=False)
    
    await ctx.send(embed=embed)
    
  @commands.hybrid_command(brief="Shows the help page")
  async def help(self, ctx, command: Optional[Literal['Collect List', 'Dex', 'Disable', 'Enable', 'Identify', 'Moveset', 'Nature', 'Price', 'Shiny Hunt', 'Shiny Rate', 'Spawnrate', 'Stats', 'Toggle', "Who's that Pokémon", 'Weakness', 'Whitelist']]):
    embed=discord.Embed(title="Pokétox", description="Use the menu below to see how to use commands! Checkout Pokétox [Terms of Service](http://poketox.me/tos)", color=0x2F3136)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/875526899386953779/d46976087eef1662db19c8272ebb57e4.png")
    embed.add_field(name="About Me", value="Poketwo reimagined — Assists you with catching, price checks pokémons, automatically pings Shiny Hunters, and much more.", inline=False)
    embed.add_field(name="<:developer:964340773367726101> Developer", value="[Future#0811](https://discord.com/users/790788488983085056)", inline=True)
    embed.add_field(name="🔗 Links", value="[Pokétox Website](http://poketox.me/)\n[Support Server](https://discord.gg/YmVA2ah5tE)\n[Bot Invite](https://discord.com/oauth2/authorize?client_id=875526899386953779&scope=bot%20applications.commands&permissions=388168)", inline=True)
    await ctx.send(embed=embed, view=DropdownView(ctx))
    
    if command == "Collect List": #Done
        await self.collectlist(ctx)
        
    if command == "Dex": #Done
        await self.dex(ctx)
        
    if command == "Disable": #Done
        await self.disable(ctx)
        
    if command == "Enable": #Done
        await self.enable(ctx)
        
    if command == "Identify": #Done
        await self.identify(ctx)
        
    if command == "Moveset": #Done
        await self.moveset(ctx)
        
    if command == "Nature": #Done
        await self.nature(ctx)
        
    if command == "Price": #Done
        await self.price(ctx)
        
    if command == "Shiny Hunt": #Done
        await self.shinyhunt(ctx)
        
    if command == "Shiny Rate": #Done
        await self.shinyrate(ctx)
        
    if command == "Spawn Rate":
        await self.spawnrate(ctx) #Done
        
    if command == "Stats": #Done
        await self.stats(ctx)
        
    if command == "Toggle": #Done
        await self.toggle(ctx)
        
    if command == "Weakness": #Done
        await self.weakness(ctx)
        
     if command == "Whitelist": #Done
        await self.whitelist(ctx)
        
     if command == "Who's that Pokémon":
        await self.wtp(ctx)

async def setup(bot):
    print("Loaded Help")
    await bot.add_cog(Help(bot))
