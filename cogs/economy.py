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
            return await ctx.reply(embed=embed)

        if (
            models.deaccent(message.content.lower().replace("′", "'"))
            not in species.correct_guesses
        ):
            embed=discord.Embed(title="Wrong", description=f"The pokemon was **{species.name}**. You can start another one with `{ctx.prefix}spawn easy`", color=0x36393F)
            return message.channel.send(embed=embed)

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
    async def medium(self, ctx, is_practice="n"):
        if ctx.guild.id != 815598238820335668 and practice != "practice":
            embed=discord.Embed(title="Wrong Server", description=f"Please use the [Official Pokétox Server](https://discord.gg/mhcjdJkxn6) for spawns! If you want to play without the rewards you can run`{ctx.prefix}spawn practice`", color=0x36393F)
            embed.add_field(name="Official Pokétox Server", value="https://discord.gg/mhcjdJkxn6", inline=False)
            return await ctx.send(embed=embed)

        if is_practice == "practice":
            amount = 0
        else:
            amount = random.randint(30, 40)

        species = self.bot.data.random_spawn()

        gamemode = 1

        elif gamemode == 1:
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
            return await ctx.reply(embed=embed)

        if (
            models.deaccent(message.content.lower().replace("′", "'"))
            not in species.correct_guesses
        ):
            embed=discord.Embed(title="Wrong", description=f"The pokemon was **{species.name}**. You can start another one with `{ctx.prefix}spawn medium`", color=0x36393F)
            return message.channel.send(embed=embed)
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
    async def hard(self, ctx, is_practice="n"):
        if ctx.guild.id != 815598238820335668 and practice != "practice":
            embed=discord.Embed(title="Wrong Server", description=f"Please use the [Official Pokétox Server](https://discord.gg/mhcjdJkxn6) for spawns! If you want to play without the rewards you can run`{ctx.prefix}spawn practice`", color=0x36393F)
            embed.add_field(name="Official Pokétox Server", value="https://discord.gg/mhcjdJkxn6", inline=False)
            return await ctx.send(embed=embed)

        if is_practice == "practice":
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
            return await ctx.reply(embed=embed)

        if (
            models.deaccent(message.content.lower().replace("′", "'"))
            not in species.correct_guesses
        ):
            embed=discord.Embed(title="Wrong", description=f"The pokemon was **{species.name}**. You can start another one with `{ctx.prefix}spawn hard`", color=0x36393F)
            return message.channel.send(embed=embed)

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

      
import discord
from discord.ext import commands
from helpers.converters import FetchUserConverter

from datetime import datetime, timedelta
from helpers import checks
import math

class Admin(commands.Cog):
    """Admin"""

    def __init__(self, bot):
        self.bot = bot
    
    async def is_banker(self, ctx):
        return ctx.guild.get_role(819688054276751381) in ctx.author.roles

    @checks.is_banker()
    @commands.command(aliases=("susp",))
    async def suspend(self, ctx, users: commands.Greedy[FetchUserConverter]):
        await self.bot.mongo.db.member.update_many(
            {"_id": {"$in": [x.id for x in users]}},
            {"$set": {"suspended": True}},
        )
        users_msg = ", ".join(f"**{x}**" for x in users)
        await ctx.send(f"Suspended {users_msg}.")
    
    @checks.is_banker()
    @commands.command(aliases=("usp",))
    async def unsuspend(self, ctx, users: commands.Greedy[FetchUserConverter]):
        await self.bot.mongo.db.member.update_many(
            {"_id": {"$in": [x.id for x in users]}},
            {"$set": {"suspended": False}},
        )
        users_msg = ", ".join(f"**{x}**" for x in users)
        await ctx.send(f"Unsuspended {users_msg}.")
    
    @checks.is_banker()
    @commands.command(aliases = ["ab"])
    async def addbal(self, ctx, user: FetchUserConverter, amount=0):
        u = await self.bot.mongo.fetch_member_info(user)
        if u is None:
            return await ctx.send(f"**{user.name}** needs to run `{ctx.prefix}start`")
        elif u.suspended:
            return await ctx.send(f"**{user.name}** is suspended")

        await self.bot.mongo.update_member(user, {"$inc": {"balance": amount}})
        await self.bot.mongo.update_member(ctx.author, {"$inc": {"banker_balance": -1*amount}})
        await ctx.send(f"Gave **{user}** {amount} tokens.")
    
    @commands.is_owner()
    @commands.command(aliases = ["ap"])
    async def addpoints(self, ctx, user: FetchUserConverter, amount=0):
        u = await self.bot.mongo.fetch_member_info(user)
        if u is None:
            return await ctx.send(f"**{user.name}** needs to run `{ctx.prefix}start`")
        elif u.suspended:
            return await ctx.send(f"**{user.name}** is suspended")
        elif not u.event_activated:
            return await ctx.send(f"**{user.name}** is not in the event.")

        await self.bot.mongo.update_member(user, {"$inc": {"points": amount}})
        await ctx.send(f"Gave **{user}** {amount} points.")
    
    @checks.is_banker()
    @commands.command(aliases = ["aub"])
    async def add_untrack_bal(self, ctx, user: FetchUserConverter, amount=0):
        u = await self.bot.mongo.fetch_member_info(user)
        if u is None:
            return await ctx.send(f"**{user.name}** needs to run `{ctx.prefix}start`")
        elif u.suspended:
            return await ctx.send(f"**{user.name}** is suspended")

        await self.bot.mongo.update_member(user, {"$inc": {"balance": amount}})
        await ctx.send(f"Gave **{user}** {amount} tokens.")
    
    @checks.is_banker()
    @commands.command(aliases = ["sb"])
    async def showbal(self, ctx, user: FetchUserConverter):
        u = await self.bot.mongo.fetch_member_info(user)
        if u is None:
            return await ctx.send(f"**{user.name}** needs to run `{ctx.prefix}start`")
        elif u.suspended:
            return await ctx.send(f"**{user.name}** is suspended")

        embed = discord.Embed(color=0xEB4634)
        embed.title =f"{user.display_name}'s balance"
        embed.add_field(name="Tokens", value=f"{u.balance:,}")
        return await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command(aliases = ["ae"])
    async def addeveryone(self, ctx, amount = 0):
        await self.bot.mongo.db.member.update_many(
            {},
            {"$inc": {"balance": amount}},
        )
        return await ctx.send(f"Gave everyone {amount} tokens!")

    @commands.is_owner()
    @commands.command(aliases = [])
    async def reset_bonus(self, ctx):
        await self.bot.mongo.db.member.update_many(
            {},
            {"$set": {"has_collected": False}},
        )
        return await ctx.send(f"Reset eveyone's event collect!")
    
    @commands.is_owner()
    @commands.command(aliases = ["abb"])
    async def addbankerbal(self, ctx, user: FetchUserConverter, amount = 0):
        await self.bot.mongo.update_member(user, {"$inc": {"banker_balance": amount}})
        return await ctx.send(f"Gave **{user}** {amount} banker tokens.")
    
    @commands.is_owner()
    @commands.command(aliases = ["rbb"])
    async def resetbankerbalance(self, ctx, user: FetchUserConverter):
        member = await self.bot.mongo.fetch_member_info(ctx.author)
        amount = member.banker_balance*-1
        await self.bot.mongo.update_member(user, {"$inc": {"banker_balance": amount}})
        return await ctx.send(f"Gave **{user}** {amount} banker tokens.")
    
def setup(bot):
    bot.add_cog(Admin(bot))
      
def setup(bot):
    bot.add_cog(Minigame(bot))
