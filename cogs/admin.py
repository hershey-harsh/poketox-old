import discord
from discord.ext import commands
from helpers.converters import FetchUserConverter

from datetime import datetime, timedelta
from helpers import checks
import math
import requests

from typing import Literal, Optional

class Admin(commands.Cog):
    """Admin"""

    def __init__(self, bot):
        self.bot = bot
    
    async def is_banker(self, ctx):
        return ctx.guild.get_role(929227238166114306) in ctx.author.roles
    
    @commands.is_owner()
    @commands.command()
    async def commandlog(self, ctx):
        await ctx.send(file=discord.File("Logs/logging.txt"), ephemeral=True)
    
    @commands.is_owner()
    @commands.command()
    async def sync(self, ctx, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*"]] = None) -> None:
        if not guilds:
            if spec == "~":
                fmt = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                fmt = await ctx.bot.tree.sync(guild=ctx.guild)
            else:
                fmt = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(fmt)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        fmt = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                fmt += 1

        await ctx.send(f"Synced the tree to {fmt}/{len(guilds)} guilds.")

    @commands.is_owner()
    @commands.command(aliases=["sp"])
    async def suspend(self, ctx, users: commands.Greedy[FetchUserConverter], *, reason: str = None):
        
        await self.bot.mongo.db.member.update_many(
            {"_id": {"$in": [x.id for x in users]}},
            {"$set": {"suspended": True, "suspension_reason": reason}},
        )
        
        users_msg = ", ".join(f"**{x}**" for x in users)
        await ctx.send(f"Suspended {users_msg} for {reason}")
    
    @commands.is_owner()
    @commands.command(aliases=["usp"])
    async def unsuspend(self, ctx, users: commands.Greedy[FetchUserConverter]):
        await self.bot.mongo.db.member.update_many(
            {"_id": {"$in": [x.id for x in users]}},
            {"$set": {"suspended": False}},
        )
        users_msg = ", ".join(f"**{x}**" for x in users)
        await ctx.send(f"Unsuspended {users_msg}.")
        
    @commands.is_owner()
    @commands.command(aliases=["rsc"])
    async def resetspawncount(self, ctx):
                await self.bot.mongo.update_guild(
                        ctx.guild, {"$set": {"spawn_count": "0"}}
                )
                await ctx.send(f"Reseted Spawn Count for {ctx.guild}")
    
    @commands.is_owner()
    @commands.command()
    async def genspawn(self, ctx, num):
              url = f"https://server.poketwo.io/image?time=day&species={num}"
        
              response = requests.get(url)
              file = open("pokemon.png", "wb")
              file.write(response.content)
              file.close()
              image = discord.File(f"pokemon.png", filename="pokemon.png")
              embed=discord.Embed(color=0x2F3136)
              embed.set_image(url="attachment://pokemon.png")
              await ctx.send(embed=embed, file=image)
    
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
        
    @checks.is_banker()
    @commands.command(aliases = ["rb"])
    async def removebal(self, ctx, user: FetchUserConverter, amount=0):
        u = await self.bot.mongo.fetch_member_info(user)
        if u is None:
            return await ctx.send(f"**{user.name}** needs to run `{ctx.prefix}start`")
        elif u.suspended:
            return await ctx.send(f"**{user.name}** is suspended")

        await self.bot.mongo.update_member(user, {"$inc": {"balance": -amount}})
        await self.bot.mongo.update_member(ctx.author, {"$inc": {"banker_balance": -1*amount}})
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
    
async def setup(bot):
    await bot.add_cog(Admin(bot))
