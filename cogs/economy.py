import asyncio
import math
import random
from datetime import datetime, timedelta
from helpers.converters import FetchUserConverter
import discord
from discord.ext import commands
from helpers import checks, helper
import math

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
