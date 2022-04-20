import asyncio
import math
import random
from datetime import datetime, timedelta
from helpers.converters import FetchUserConverter
import discord
from discord.ext import commands
from helpers import checks, helper
import math
import asyncio
import math
import random
from datetime import datetime, timedelta

import config
import discord
from discord.ext import commands
from helpers import checks, helper

from data import models

# from helpers.puzzle import PuzzleType, Puzzle

from data import models


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
        await ctx.send(
            f"Welcome! You can run `{ctx.prefix}help` to see the variety of minigames we have. At any time, you can contact one of the bankers to get money or withdraw tokens."
        )
        
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
        if amount <= 0:
            return await ctx.send("Nice Try")

        if start == "start":
            member = await self.bot.mongo.fetch_member_info(ctx.author)
            bal = member.balance

            if bal < amount:
                return await ctx.send(
                    f"You don't have enough tokens to play (min: {amount})"
                )

            outcome = config.RATES(amount)
            if outcome:
                dice_roll = random.randint(4, 6)
            else:
                dice_roll = random.randint(1, 3)

            embed = discord.Embed(color=0xEB4634)
            embed.title = f"Dice Roll — {amount}"
            embed.add_field(name="Roll", value=f"You rolled a **{dice_roll}**.")
            if dice_roll >= 4:
                await self.bot.mongo.update_member(
                    ctx.author, {"$inc": {"balance": amount}}
                )
                embed.add_field(
                    name="Winnings",
                    value=f"You won **{amount*2} tokens**!",
                    inline=False,
                )
            else:
                await self.bot.mongo.update_member(
                    ctx.author, {"$inc": {"balance": -1 * amount}}
                )
                embed.add_field(
                    name="Winnings", value=f"You won **0 tokens.**", inline=False
                )
            return await ctx.send(f"> <@!{ctx.author.id}>", embed=embed)
        else:
            embed = discord.Embed(
                title=f"Dice Roll",
                description=f"You roll a 6 sided dice. If the dice is at least 4, you win 2x the amount you entered with. Do `{ctx.prefix}diceroll start <amount>` to play!",
                color=0xEB4634,
            )
            return await ctx.send(embed=embed)

    @checks.has_started()
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.command(aliases=["cf", "coin"])
    async def coinflip(self, ctx, start="about", amount=10, choice="heads"):
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
                return await ctx.send(
                    f"You don't have enough tokens to play (min: {amount})"
                )

            outcome = config.RATES(amount)
            if outcome:
                flip = choice
            else:
                flip = "tails" if choice == "heads" else "heads"

            embed = discord.Embed(color=0xEB4634)
            embed.title = f"Coinflip — {amount}"
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
                embed.add_field(
                    name="Winnings",
                    value=f"You won **{amount*2} tokens**!",
                    inline=False,
                )
            else:
                await self.bot.mongo.update_member(
                    ctx.author, {"$inc": {"balance": -1 * amount}}
                )
                embed.add_field(
                    name="Winnings", value=f"You won **0 tokens.**", inline=False
                )
            return await ctx.send(f"> <@!{ctx.author.id}>", embed=embed)
        else:
            embed = discord.Embed(
                title=f"Coin Flip",
                description=f"You flip a coin, if the coin lands on heads, you win 2x the amount you entered with. Do `{ctx.prefix}coinflip start <amount>` to play!",
                color=0xEB4634,
            )
            return await ctx.send(embed=embed)
    
    @commands.group(invoke_without_command=True)
    async def spawn(self, ctx):
        return None
        
    @checks.has_started()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @spawn.command(invoke_without_command=True)
    async def easy(self, ctx, practice="n"):
        if ctx.guild.id != 815598238820335668 and practice != "practice":
            embed=discord.Embed(title="Wrong Server", description=f"Please use the [Official Pokétox Server](https://discord.gg/mhcjdJkxn6) for spawns! If you want to play without the rewards you can run`{ctx.prefix}spawn practice`", color=0x36393F)
            embed.add_field(name="Official Pokétox Server", value="https://discord.gg/mhcjdJkxn6", inline=False)
            return await ctx.send(embed=embed)

        if practice == "practice":
            amount = 0
        else:
            amount = random.randint(10, 30)

        # puzzle = Puzzle(self.bot, PuzzleType.Scramble)

        species = self.bot.data.random_spawn()
        embed = discord.Embed(
            title=f"Spawn",
            description=f"Hint: The first letter is **{species.name[0]}**. Unscramble this pokemon for **{amount}** tokens **{helper.scramble(species.name)}**",
            color=0x36393F,
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
            embed=discord.Embed(title="Times Up", description=f"The pokemon was **{species.name}**. You can start another one with `{ctx.prefix}spawn easy`", color=0x36393F)
            return await ctx.send(embed=embed)

        if (
            models.deaccent(message.content.lower().replace("′", "'"))
            not in species.correct_guesses
        ):
            embed=discord.Embed(title="Wrong", description=f"The pokemon was **{species.name}**. You can start another one with `{ctx.prefix}spawn easy`", color=0x36393F)
            return await message.channel.send(embed=embed)

        embed = discord.Embed(
            title=f"Correct",
            description=f"You have been awarded **{amount}**",
            color=0x36393F,
        )
        await self.bot.mongo.update_member(
            ctx.author,
            {"$inc": {"balance": amount}},
        )
        return await message.reply(embed=embed)
    
    @checks.has_started()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @spawn.command()
    async def medium(self, ctx, practice="n"):
        if ctx.guild.id != 815598238820335668 and practice != "practice":
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
                color=0x36393F,
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
            embed=discord.Embed(title="Times Up", description=f"The pokemon was **{species.name}**. You can start another one with `{ctx.prefix}spawn medium`", color=0x36393F)
            return await ctx.send(embed=embed)

        if (
            models.deaccent(message.content.lower().replace("′", "'"))
            not in species.correct_guesses
        ):
            embed=discord.Embed(title="Wrong", description=f"The pokemon was **{species.name}**. You can start another one with `{ctx.prefix}spawn medium`", color=0x36393F)
            return await message.channel.send(embed=embed)
        embed = discord.Embed(
            title=f"Correct",
            description=f"You have been awarded **{amount}**",
            color=0x36393F,
        )
        await self.bot.mongo.update_member(
            ctx.author,
            {"$inc": {"balance": amount}},
        )
        return await message.reply(embed=embed)
    
    @checks.has_started()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @spawn.command()
    async def hard(self, ctx, practice="n"):
        if ctx.guild.id != 815598238820335668 and practice != "practice":
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
                color=0x36393F,
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
            embed=discord.Embed(title="Times Up", description=f"The pokemon was **{species.name}**. You can start another one with `{ctx.prefix}spawn hard`", color=0x36393F)
            return await ctx.send(embed=embed)

        if (
            models.deaccent(message.content.lower().replace("′", "'"))
            not in species.correct_guesses
        ):
            embed=discord.Embed(title="Wrong", description=f"The pokemon was **{species.name}**. You can start another one with `{ctx.prefix}spawn hard`", color=0x36393F)
            return await message.channel.send(embed=embed)

        embed = discord.Embed(
            title=f"Correct",
            description=f"You have been awarded **{amount}**",
            color=0x36393F,
        )
        await self.bot.mongo.update_member(
            ctx.author,
            {"$inc": {"balance": amount}},
        )
        return await message.reply(embed=embed)
      
def setup(bot):
    bot.add_cog(Minigame(bot))
