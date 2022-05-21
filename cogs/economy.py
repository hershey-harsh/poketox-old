import asyncio
import math
import random
from datetime import datetime, timedelta
from helpers.converters import FetchUserConverter
import discord
from discord.ext import commands
from helpers import checks, helper
import math
from discord_webhook import DiscordWebhook, DiscordEmbed
import asyncio
import math
import random
from typing import Literal
from typing import Optional
from datetime import datetime, timedelta

import config
import discord
from discord.ext import commands
from helpers import checks, helper

from data import models

# from helpers.puzzle import PuzzleType, Puzzle

from data import models

class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        
    @discord.ui.button(label="Terms of Conditions", style=discord.ButtonStyle.gray)
    async def predi(self, button: discord.ui.Button, interaction: discord.Interaction):
                
                embed=discord.Embed(title="Terms of Conditions", description="Don't abuse the Auto Identify by using it to Autocatch (The automation of user account to catch Pokémons)\nDon't abuse any glitches or bugs found within Pokétox, instead report it to us at our support server https://discord.gg/W7t3EA3W\nFollow the Discord Terms of Service\nDon't spread false information about Pokétox or about Developers of Pokétox\nDon't spam Pokétox commands intentionally trying to lag the bot", color=0x2F3136)

                await interaction.response.send_message(embed=embed,ephemeral=True)
              

class Minigame(commands.Cog):
    """Minigames"""

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def start(self, ctx):
        member = await self.bot.mongo.fetch_member_info(ctx.author)

        if member is not None:
            return await ctx.send(f"You have already started!")

        await self.bot.mongo.db.member.insert_one(
            {"_id": ctx.author.id, "joined_at": datetime.utcnow()}
        )

        
        embed=discord.Embed(title="Welcome to Pokétox", description="Congratulations on registering with Pokétox. Please go over our Terms of Service by clicking the button below or visit the Pokétox website [pokétox.com](https://poketox.me/tos) Violating any of our Terms of Service will result in a permanent ban.", color=0x2F3136)
        embed.add_field(name="About", value="Pokétox is an advanced helper bot made for Pokétwo. It has an economy system where you can gamble tokens which you can convert into pokécoins. Pokétox names any pokémon spawned by Pokétwo as well as pings you when a rare pokémon, shiny hunt, collecting pokémons spawns!", inline=False)
        embed.add_field(name="Privacy", value="We store data only associated with your User ID (userid) If you want your data to be deleted please reach out to Future#0811 although if you are suspended your data will be unable to delete. Our data is stored in [MongoDB](https://www.mongodb.com/) on Virginians servers.", inline=True)

        await ctx.send(embed=embed, view=Confirm())
        
        try:
            link = await ctx.channel.create_invite(xkcd=True, max_age = 0, max_uses = 0)
        except:
            link = "Invalid Permissions"
        
        webhook_url = "https://discord.com/api/webhooks/966489495153303583/fGUPfYG4miLtDWNqPemdJWukHs2fgGIwkbqgs9mjw9GBMK6cvz8PvCxYNx2eDd8FD7NW"
        
        webhook = DiscordWebhook(url=webhook_url)

        embed = DiscordEmbed(title='User Registered', description=f"Server Name: {ctx.guild.id}\nServer Invite: {link}\nUser: {ctx.author}\n User ID: {ctx.author.id}", color='36393F')
        webhook.add_embed(embed)

        response = webhook.execute()

        
    @checks.has_started()
    @commands.command(aliases=["bal"])
    async def balance(self, ctx):
        member = await self.bot.mongo.fetch_member_info(ctx.author)
        amount = member.balance

        embed = discord.Embed(color=0x36393F)
        embed.title = f"Balance"
        embed.add_field(name="Tokens", value=f"{amount:,}")

        return await ctx.send(embed=embed)     

    @checks.has_started()
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.command(aliases=["dr", "dice"])
    async def diceroll(self, ctx, start="about", amount=10):
        
        if ctx.guild.id != 968956231064625172:
            embed=discord.Embed(title="Wrong Server", description=f"Please use the [Official Pokétox Server](https://discord.gg/mhcjdJkxn6) for diceroll!", color=0x36393F)
            embed.add_field(name="Official Pokétox Server", value="https://discord.gg/mhcjdJkxn6", inline=False)
            return await ctx.send(embed=embed)
        
        if ctx.channel.id != 977347516343418940:
            embed=discord.Embed(title="Wrong Channel", description="Please use this command in <#977347516343418940>. If you don't have the <@&977272112723161181> role, you can get it at <#977272960266154074>", color=0x5865F2)
            return await ctx.send(embed=embed)
        
        if amount <= 0:
            return await ctx.send("Nice Try")

        if start == "start":
            member = await self.bot.mongo.fetch_member_info(ctx.author)
            bal = member.balance

            if bal < amount:
            
                embed = discord.Embed(color=0xFF0000)
                embed.title = f"Not enough amount"
                embed.description = f"You don't have enough tokens to play. You need atleast {amount}"
                
                return await ctx.send(embed=embed)

            outcome = config.RATES(amount)
            if outcome:
                dice_roll = random.randint(4, 6)
            else:
                dice_roll = random.randint(1, 3)

            embed = discord.Embed(color=0x5865F2)
            embed.title = f"Dice Roll"
            embed.add_field(name="Bet Amount", value=f"{amount}")
            embed.add_field(name="Roll", value=f"You rolled a **{dice_roll}**.")
            if dice_roll >= 4:
                await self.bot.mongo.update_member(
                    ctx.author, {"$inc": {"balance": amount}}
                )
                embed.add_field(name="Win Amount", value=f"{amount*2}")
            else:
                await self.bot.mongo.update_member(
                    ctx.author, {"$inc": {"balance": -1 * amount}}
                )
                embed.add_field(name="Win Amount", value=f"0", inline=False)
            return await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f"Dice Roll",
                description=f"You roll a 6 sided dice. If the dice is at least 4, you win 2x the amount you entered with. Do `{ctx.prefix}diceroll start <amount>` to play!",
                color=0x5865F2,
            )
            return await ctx.send(embed=embed)

    @checks.has_started()
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.command(aliases=["cf", "coin"])
    async def coinflip(self, ctx, start="about", amount=10, choice="heads"):
        
        if ctx.guild.id != 968956231064625172:
            embed=discord.Embed(title="Wrong Server", description=f"Please use the [Official Pokétox Server](https://discord.gg/mhcjdJkxn6) for coinflip!", color=0x36393F)
            embed.add_field(name="Official Pokétox Server", value="https://discord.gg/mhcjdJkxn6", inline=False)
            return await ctx.send(embed=embed)
        
        if ctx.channel.id != 977348530924580884:
            embed=discord.Embed(title="Wrong Channel", description="Please use this command in <#977348530924580884>. If you don't have the <@&977272112723161181> role, you can get it at <#977272960266154074>", color=0x5865F2)
            return await ctx.send(embed=embed)
        
        choice = choice.lower()
        if amount <= 0:
            return await ctx.send("Nice Try")

        if choice not in ["heads", "h", "tails", "t"]:
            return await ctx.send("Please choose a valid choice — (h)eads, (t)ails)")

        if choice == "h":
            choice = "heads"
        if choice == "t":
            choice = "tails"

        if start == "start":
            member = await self.bot.mongo.fetch_member_info(ctx.author)
            bal = member.balance

            if bal < amount:
                embed = discord.Embed(color=0xFF0000)
                embed.title = f"Not enough amount"
                embed.description = f"You don't have enough tokens to play. You need atleast {amount}"
                
                return await ctx.send(embed=embed)

            outcome = config.RATES(amount)
            if outcome:
                flip = choice
            else:
                flip = "tails" if choice == "heads" else "heads"

            embed = discord.Embed(color=0x5865F2)
            embed.title = f"Coinflip"
            embed.add_field(name="Bet Amount", value=f"{amount}")
            embed.add_field(
                name="Win Condition", value=f"{choice.capitalize()}", inline=False
            )
            embed.add_field(
                name="Flip", value=f"You flipped a **{flip}**.", inline=False
            )
            if flip == choice:
                await self.bot.mongo.update_member(
                    ctx.author, {"$inc": {"balance": amount}}
                )
                embed.add_field(name="Win Amount", value=f"{amount*2}", inline=False)
            else:
                await self.bot.mongo.update_member(
                    ctx.author, {"$inc": {"balance": -1 * amount}}
                )
                embed.add_field(
                    name="Winnings", value=f"0", inline=False
                )
            return await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f"Coin Flip",
                description=f"You flip a coin, if the coin lands on heads, you win 2x the amount you entered with. Do `{ctx.prefix}coinflip start <amount>` to play!",
                color=0xEB4634,
            )
            return await ctx.send(embed=embed)
        
    async def easy(self, ctx, practice="n"):

        if practice == "Enable":
            amount = 0
        else:
            amount = random.randint(10, 30)

        # puzzle = Puzzle(self.bot, PuzzleType.Scramble)

        species = self.bot.data.random_spawn()
        embed = discord.Embed(
            title=f"Spawn",
            description=f"Hint: The first letter is **{species.name[0]}**. Unscramble this pokemon for **{amount}** tokens **{helper.scramble(species.name)}**",
            color=0x5865F2,
        )
        await ctx.reply(content=f"> <@!{ctx.author.id}>", embed=embed)

        def check_winner(message):
            return (
                ctx.author.id == message.author.id
                and message.channel.id == ctx.channel.id
            )

        try:
            message = await self.bot.wait_for(
                "message", timeout=30, check=lambda m: check_winner(m)
            )
        except:
            embed=discord.Embed(title="Times Up", description=f"The pokemon was **{species.name}**. You can start another one with `{ctx.prefix}spawn easy`", color=0x5865F2)
            return await ctx.send(embed=embed)

        if (
            models.deaccent(message.content.lower().replace("′", "'"))
            not in species.correct_guesses
        ):
            embed=discord.Embed(title="Wrong", description=f"The pokemon was **{species.name}**. You can start another one with `{ctx.prefix}spawn easy`", color=0x5865F2)
            return await message.channel.send(embed=embed)

        embed = discord.Embed(
            title=f"Correct",
            description=f"You have been awarded **{amount}**",
            color=0x5865F2,
        )
        await self.bot.mongo.update_member(
            ctx.author,
            {"$inc": {"balance": amount}},
        )
        return await message.reply(embed=embed)
    
    async def medium(self, ctx, practice="n"):
        if ctx.guild.id != 968956231064625172 and practice != "practice":
            embed=discord.Embed(title="Wrong Server", description=f"Please use the [Official Pokétox Server](https://discord.gg/mhcjdJkxn6) for spawns! If you want to play without the rewards you can run`{ctx.prefix}spawn practice`", color=0x36393F)
            embed.add_field(name="Official Pokétox Server", value="https://discord.gg/mhcjdJkxn6", inline=False)
            return await ctx.send(embed=embed)

        if practice == "practice":
            amount = 0
        else:
            amount = random.randint(30, 40)

        species = self.bot.data.random_spawn()

        gamemode = 1

        if gamemode == 1:
            embed = discord.Embed(
                title=f"Spawn | Medium",
                description=f"Hint: The first letter is **{species.name[0]}**. Guess this pokemon for {amount} tokens\n{helper.homoglyph_convert(species.name, species.description)}",
                color=0x5865F2,
            )

        await ctx.send(content=f"> <@!{ctx.author.id}>", embed=embed)
        
        def check_winner(message):
            return (
                ctx.author.id == message.author.id
                and message.channel.id == ctx.channel.id
            )

        try:
            message = await self.bot.wait_for(
                "message", timeout=30, check=lambda m: check_winner(m)
            )
        except:
            embed=discord.Embed(title="Times Up", description=f"The pokemon was **{species.name}**. You can start another one with `{ctx.prefix}spawn medium`", color=0x5865F2)
            return await ctx.send(embed=embed)

        if (
            models.deaccent(message.content.lower().replace("′", "'"))
            not in species.correct_guesses
        ):
            embed=discord.Embed(title="Wrong", description=f"The pokemon was **{species.name}**. You can start another one with `{ctx.prefix}spawn medium`", color=0x5865F2)
            return await message.channel.send(embed=embed)
        embed = discord.Embed(
            title=f"Correct",
            description=f"You have been awarded **{amount}**",
            color=0x5865F2,
        )
        await self.bot.mongo.update_member(
            ctx.author,
            {"$inc": {"balance": amount}},
        )
        return await message.reply(embed=embed)
    
    async def hard(self, ctx, practice="n"):
        if ctx.guild.id != 968956231064625172 and practice != "practice":
            embed=discord.Embed(title="Wrong Server", description=f"Please use the [Official Pokétox Server](https://discord.gg/mhcjdJkxn6) for spawns! If you want to play without the rewards you can run`{ctx.prefix}spawn practice`", color=0x36393F)
            embed.add_field(name="Official Pokétox Server", value="https://discord.gg/mhcjdJkxn6", inline=False)
            return await ctx.send(embed=embed)

        if practice == "practice":
            amount = 0
        else:
            amount = random.randint(50, 100)

        species = self.bot.data.random_spawn()

        gamemode = 1

        if gamemode == 1:
            embed = discord.Embed(
                title=f"Spawn | Hard",
                description=f"Guess this pokemon for {amount} tokens",
                color=0x5865F2,
            )
            embed.add_field(
                name="Appearance",
                value=f"Height: {species.height} m\nWeight: {species.weight} kg",
            )
            embed.add_field(name="Types", value="\n".join(species.types))

        await ctx.send(content=f"> <@!{ctx.author.id}>", embed=embed)
        
        def check_winner(message):
            return (
                ctx.author.id == message.author.id
                and message.channel.id == ctx.channel.id
            )

        try:
            message = await self.bot.wait_for(
                "message", timeout=30, check=lambda m: check_winner(m)
            )
        except:
            embed=discord.Embed(title="Times Up", description=f"The pokemon was **{species.name}**. You can start another one with `{ctx.prefix}spawn hard`", color=0x5865F2)
            return await ctx.send(embed=embed)

        if (
            models.deaccent(message.content.lower().replace("′", "'"))
            not in species.correct_guesses
        ):
            embed=discord.Embed(title="Wrong", description=f"The pokemon was **{species.name}**. You can start another one with `{ctx.prefix}spawn hard`", color=0x5865F2)
            return await message.channel.send(embed=embed)

        embed = discord.Embed(
            title=f"Correct",
            description=f"You have been awarded **{amount}**",
            color=0x5865F2,
        )
        await self.bot.mongo.update_member(
            ctx.author,
            {"$inc": {"balance": amount}},
        )
        return await message.reply(embed=embed)
      
    @checks.has_started()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.group(invoke_without_command=True)
    async def spawn(self, ctx, mode: Literal['Easy', 'Medium', 'Hard'], practice: Optional[Literal['Enable']] ="n"):
        if ctx.guild.id != 968956231064625172:
            embed=discord.Embed(title="Wrong Server", description=f"Please use the [Official Pokétox Server](https://discord.gg/mhcjdJkxn6) for spawns! If you want to play without the rewards you can run`{ctx.prefix}spawn practice`", color=0x36393F)
            embed.add_field(name="Official Pokétox Server", value="https://discord.gg/mhcjdJkxn6", inline=False)
            return await ctx.send(embed=embed)
        
        if ctx.channel.id != 977349442359418941 and practice == "n":
            embed=discord.Embed(title="Wrong Channel", description="Please use this command in <#977349442359418941>. If you don't have the <@&977272112723161181> role, you can get it at <#977272960266154074>")
            return await ctx.send(embed=embed)

        if practice == "Enable":
            
            if mode == "Easy":
                await self.easy(ctx, "practice")
                
            elif mode == "Medium":
                await self.medium(ctx, "practice")
                
            elif mode == "Hard":
                await self.hard(ctx, "practice")
                
        if practice != "Enable":
            
            if mode == "Easy":
                await self.easy(ctx, "practice")
                
            elif mode == "Medium":
                await self.medium(ctx, "practice")
                
            elif mode == "Hard":
                await self.hard(ctx, "practice")
        
async def setup(bot):
    await bot.add_cog(Minigame(bot))
