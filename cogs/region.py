import discord
from discord.ext import commands
from discord.ext.menus.views import ViewMenuPages
from helpers.converters import FetchUserConverter, SpeciesConverter
from helpers import checks, context
import datetime
from datetime import datetime, timedelta
from typing import List
from discord import File, Member
from helpers.pagination import AsyncEmbedListPageSource

import random
import asyncio

class Region(commands.Cog):
    """For region."""

    def __init__(self, bot):
        self.bot = bot

    async def doc_to_species(self, doc):
        for x in doc.keys():
            if x != "_id":
                if self.bot.data.species_by_number(int(x)):
                    yield self.bot.data.species_by_number(int(x))
                    
    @checks.has_started()
    @commands.hybrid_group(aliases=("rl","regionallist",), invoke_without_command=True, slash_command=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def regionhunt(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        result = await self.bot.mongo.db.regionlist.find_one({"_id": member.id})
        
        pages = ViewMenuPages(
            source=AsyncEmbedListPageSource(
                self.doc_to_species(result or {}),
                title=str(member),
                format_item=lambda x: x.name,
            )
        )

        try:
            await pages.start(ctx)
        except IndexError:
            await ctx.send("No regions found.")
        
    @checks.has_started()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @regionhunt.command(slash_command=True)
    async def view(self, ctx, *, member: discord.Member = None):

        """Allows members to keep track of the hunters of a region"""
      
        if member is None:
            member = ctx.author

        result = await self.bot.mongo.db.regionlist.find_one({"_id": member.id})

        pages = ViewMenuPages(
            source=AsyncEmbedListPageSource(
                self.doc_to_species(result or {}),
                title=str(member),
                format_item=lambda x: x.name,
            )
        )

        try:
            await pages.start(ctx)
        except IndexError:
            await ctx.send("No regions found.")
        
    @checks.has_started()
    @regionhunt.command(slash_command=True, brief="Adds a region to your regional list")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def add(self, ctx, *, region: SpeciesConverter):

        regions = ['Kanto', 'Johto', 'Hoenn', 'Sinnoh', 'Unova', 'Kalos', 'Alola', 'Galar', 'Hisui']
        
        if region.name.title() not in regions:
            return await ctx.send("You cannot add pokémons to regional list.")
        
        result = await self.bot.mongo.db.regionlist.update_one(
            {"_id": ctx.author.id},
            {"$set": {str(region.id): True}},
            upsert=True
        )

        if result.upserted_id or result.modified_count > 0:
            embed=discord.Embed(title="Region", description=f"Added **{region}** to your regional list", color=0x36393F)
            
            await ctx.send(
                embed=embed
            )
        
        else:
            embed=discord.Embed(title="Region", description=f"**{region}** is already on your regional list", color=0x36393F)
            
            await ctx.send(
                embed=embed, ephemeral=True #Returns ephemeral message if this command was invoked by slash.
            )
        
    @add.autocomplete('region')
    async def add_autocomplete(self, interaction: discord.Interaction, current: str) -> List[discord.app_commands.Choice[str]]:
        matches = interaction.client.data.closest_species_by_name(current)
        
        regions = ['Kanto', 'Johto', 'Hoenn', 'Sinnoh', 'Unova', 'Kalos', 'Alola', 'Galar', 'Hisui', 'Legendaries', 'Alolan-Form', 'Galarian-Form', 'Hisuian-Form']
        
        return [
            discord.app_commands.Choice(name=region, value=region)
            for region in regions if current.lower() in region.lower()
        ]

    @checks.has_started()
    @regionhunt.command(slash_command=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def multiadd(self, ctx, *, regions):
        """Adds a multiple regions to your regional list"""
        
        myList = []
        for i in regions.split(', '):
                region= self.bot.data.species_by_name(i)
                
                result = await self.bot.mongo.db.regionlist.update_one(
                        {"_id": ctx.author.id},
                        {"$set": {str(region.id): True}},
                        upsert=True,
                )
                
                if result.upserted_id or result.modified_count > 0:
                        myList.append(i.capitalize())
                        
                else:
                        await ctx.send(f"**{region}** is already on your regional list")

        embed1=discord.Embed(title="Regional Hunters", description=f"Added **{', '.join(myList)}** to your regional list", color=0x36393F)

        return await ctx.send(embed=embed1)

    @checks.has_started()
    @regionhunt.command(slash_command=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def multiremove(self, ctx, *, regions):
        """Remove multiple regions from your regional list"""
        
        myList = []
        for i in regions.split(', '):
                region= self.bot.data.species_by_name(i)
                
                result = await self.bot.mongo.db.regionlist.update_one(
                        {"_id": ctx.author.id},
                        {"$unset": {str(region.id): True}},
                        upsert=True,
                )
                
                if result.upserted_id or result.modified_count > 0:
                        myList.append(i.capitalize())
                        
                else:
                        await ctx.send(f"**{region}** is already on your regional list")

        embed=discord.Embed(title="Region", description=f"Removed **{', '.join(myList)}** from your regional list.", color=0x36393F)

        return await ctx.send(embed=embed)

    @checks.has_started()
    @regionhunt.command(slash_command=True)
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def remove(self, ctx, *, region: SpeciesConverter):
        """Remove a region from your regional List"""

        result = await self.bot.mongo.db.regionlist.update_one(
            {"_id": ctx.author.id},
            {"$unset": {str(region.id): 1}},
        )

        if result.modified_count > 0:
            embed=discord.Embed(title="Region", description=f"Removed {region} from your regional list.", color=0x36393F)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Region", description=f"**{region}** is not in your regional list.", color=0x36393F)
            await ctx.send(embed=embed, ephemeral=True)
    
    @checks.has_started()
    @regionhunt.command()
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def clear(self, ctx):
        """Clear your regional list"""
    
        result = await ctx.confirm('Your about to **clear** your regional list. Are you sure you want to continue?')
        
        if result is None:
                return await ctx.send("Time's up. Aborted.")

        if result is False:
                return await ctx.send("Aborted.")
                
        await self.bot.mongo.db.regionlist.delete_one({"_id": ctx.author.id})
        await ctx.send("Cleared your regional list.")

    @checks.has_started()
    @regionhunt.command(slash_command=True)
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def globalsearch(self, ctx, *, region: SpeciesConverter):
        """Lists the hunters of a regions"""

        users = self.bot.mongo.db.regionlist.find({str(region.id): True})
        pages = ViewMenuPages(
            source=AsyncEmbedListPageSource(
                users,
                title=f"All {region} Regional Hunters using the bot",
                format_item=lambda x: f"<@{x['_id']}>",
            )
        )

        
        await pages.start(ctx)
        
    @checks.has_started()
    @regionhunt.command(slash_command=True)
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def search(self, ctx, *, region: SpeciesConverter):
        """Lists the hunters of a regions in the server"""

        users = self.bot.mongo.db.regionlist.find({str(region.id): True, str(ctx.guild.id): True})
        pages = ViewMenuPages(
            source=AsyncEmbedListPageSource(
                users,
                title=f"{region} Regional Hunters in this server",
                format_item=lambda x: f"<@{x['_id']}>",
            )
        )

        try:
            await pages.start(ctx)
        except IndexError:
            await ctx.send("No users found.")
            

            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    @checks.has_started()
    @commands.hybrid_group(aliases=("rf","rfh",), invoke_without_command=True, slash_command=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def regionformhunt(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        result = await self.bot.mongo.db.regionformlist.find_one({"_id": member.id})
        
        pages = ViewMenuPages(
            source=AsyncEmbedListPageSource(
                self.doc_to_species(result or {}),
                title=str(member),
                format_item=lambda x: x.name,
            )
        )

        try:
            await pages.start(ctx)
        except IndexError:
            await ctx.send("No regions found.")
        
    @checks.has_started()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @regionformhunt.command(slash_command=True)
    async def view(self, ctx, *, member: discord.Member = None):

        """Allows members to keep track of the hunters of a region form"""
      
        if member is None:
            member = ctx.author

        result = await self.bot.mongo.db.regionformlist.find_one({"_id": member.id})

        pages = ViewMenuPages(
            source=AsyncEmbedListPageSource(
                self.doc_to_species(result or {}),
                title=str(member),
                format_item=lambda x: x.name,
            )
        )

        try:
            await pages.start(ctx)
        except IndexError:
            await ctx.send("No regions forms found.")
        
    @checks.has_started()
    @regionformhunt.command(slash_command=True, brief="Adds a region form to your regional forms list")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def add(self, ctx, *, region: SpeciesConverter):

        regions = ['Legendaries', 'Alolan', 'Galarian', 'Hisuian']
        
        if region.name.title() not in regions:
            return await ctx.send("You cannot add pokémons or regions your to regional forms list.")
        
        result = await self.bot.mongo.db.regionlist.update_one(
            {"_id": ctx.author.id},
            {"$set": {str(region.id): True}},
            upsert=True
        )

        if result.upserted_id or result.modified_count > 0:
            embed=discord.Embed(title="Region Forms", description=f"Added **{region}** to your regional forms list", color=0x36393F)
            
            await ctx.send(
                embed=embed
            )
        
        else:
            embed=discord.Embed(title="Region Form", description=f"**{region}** is already on your regional forms list", color=0x36393F)
            
            await ctx.send(
                embed=embed, ephemeral=True #Returns ephemeral message if this command was invoked by slash.
            )
        
    @add.autocomplete('region')
    async def add_autocomplete(self, interaction: discord.Interaction, current: str) -> List[discord.app_commands.Choice[str]]:
        matches = interaction.client.data.closest_species_by_name(current)
        
        regions = ['Legendaries', 'Alolan', 'Galarian', 'Hisuian']
        
        return [
            discord.app_commands.Choice(name=region, value=region)
            for region in regions if current.lower() in region.lower()
        ]

    @checks.has_started()
    @regionformhunt.command(slash_command=True)
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def remove(self, ctx, *, region: SpeciesConverter):
        """Remove a region from your regional List"""

        result = await self.bot.mongo.db.regionlist.update_one(
            {"_id": ctx.author.id},
            {"$unset": {str(region.id): 1}},
        )

        if result.modified_count > 0:
            embed=discord.Embed(title="Region Form", description=f"Removed {region} from your regional forms list.", color=0x36393F)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Region Form", description=f"**{region}** is not in your regional forms list.", color=0x36393F)
            await ctx.send(embed=embed, ephemeral=True)
            
    @checks.has_started()
    @regionformhunt.command()
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def clear(self, ctx):
        """Clear your regional forms list"""
    
        result = await ctx.confirm('Your about to **clear** your regional forms list. Are you sure you want to continue?')
        
        if result is None:
                return await ctx.send("Time's up. Aborted.")

        if result is False:
                return await ctx.send("Aborted.")
                
        await self.bot.mongo.db.regionlist.delete_one({"_id": ctx.author.id})
        await ctx.send("Cleared your regional forms list.")

async def setup(bot):
    print("Loaded Region")
    await bot.add_cog(Region(bot))
