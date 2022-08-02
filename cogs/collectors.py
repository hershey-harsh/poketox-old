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

async def collectping(self, ctx, species: SpeciesConverter):
    
        guild = await ctx.bot.mongo.fetch_guild(ctx.guild)
        if guild.ping_channels and ctx.channel.id not in guild.ping_channels:
            return

        users = self.bot.mongo.db.collector.find(
            {str(species.id): True, str(ctx.guild.id): True}
        )

        try:
                guild = await self.bot.mongo.db.shtimer.find_one({"_id": ctx.guild.id})
        except Exception as e:
                pass
        
        try:
                time = str(guild[str(ctx.channel.id)])
        except Exception as e:
                time = None
                pass
        
        collector_pings = []
        async for user in users:
            collector_pings.append(f"<@{user['_id']}> ")
        
        if len(collector_pings) > 0:

            if time != None:
                x = datetime.now() + timedelta(seconds=1)
                x += timedelta(seconds=int(time))
                timestamp = discord.utils.format_dt(x, 'R')
            else:
                timestamp = " "
                time=0
                
            msg = await ctx.send(f"**<:pokeball:936773252913700894> Pinging {species} Collectors**\nYou may catch {species} {timestamp} \n \n" + " ".join(collector_pings))  

            try:
                if time != 0:
                        time = str(guild[str(ctx.channel.id)])
                        await asyncio.sleep(int(time))
                        embed=discord.Embed(description=f"Post-Tag timer has expired for {species}. You may catch it now", color=0x2F3136)
                        await ctx.send(embed=embed)
                
                        await msg.edit(f"**Pinging {species} Collectors**\n \n" + " ".join(collector_pings))
            except:
                pass
        
        else:
            mess = await ctx.send(
                f"No one is collecting {species}"
            )
           
async def shinyping(self, ctx, species: SpeciesConverter):

        guild = await ctx.bot.mongo.fetch_guild(ctx.guild)
        if guild["sh_channels"] and ctx.channel.id not in guild["sh_channels"]:
            return

        users = self.bot.mongo.db.shinyhunt.find(
            {str(ctx.guild.id): True, 'shinyhunt': species.id}
        )
        
        try:
                guild = await self.bot.mongo.db.shtimer.find_one({"_id": ctx.guild.id})
        except Exception as e:
                pass
        
        try:
                time = str(guild[str(ctx.channel.id)])
        except Exception as e:
                time = None
                pass
                
        shinyhunt_pings = []
        
        async for user in users:
            shinyhunt_pings.append(f"<@{user['_id']}> ")
        
        if len(shinyhunt_pings) > 0:
                
            if time != None:
                x = datetime.now() + timedelta(seconds=1)
                x += timedelta(seconds=int(time))
                timestamp = discord.utils.format_dt(x, 'R')
            else:
                timestamp = " "
                time = 0
                
            msg = await ctx.send(
                f"**:sparkles: Pinging {species} Shiny Hunters**\n You may catch {species} {timestamp} \n \n" + " ".join(shinyhunt_pings)
            )
            
            try:
                if time != 0:
                        await asyncio.sleep(int(time))
                        embed=discord.Embed(description=f"Post-Tag timer has expired for {species}. You may catch it now", color=0x2F3136)
                        await ctx.send(embed=embed)
                
                await msg.edit(
                        f"**Pinging {species} Shiny Hunters**\n \n" + " ".join(shinyhunt_pings)
                )
                
            except:
                pass
            
        else:
            mess = await ctx.send(
                f"No one is shiny hunting {species}!"
            )

class Collectors(commands.Cog):
    """For collectors."""

    def __init__(self, bot):
        self.bot = bot

    async def doc_to_species(self, doc):
        for x in doc.keys():
            if x != "_id":
                if self.bot.data.species_by_number(int(x)):
                    yield self.bot.data.species_by_number(int(x))
                
    @checks.has_started()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.hybrid_group(invoke_without_command=True, case_insensitive=True, slash_command=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def timer(self, ctx: commands.Context, seconds, channel: discord.TextChannel=None):
                
        if channel == None:
                return
        
        if seconds == None:
                return
        
        if int(seconds) >= 120:
                return await ctx.send("Seconds have to be less than 120 seconds!")
        
        try:
                await self.bot.mongo.db.shtimer.insert_one(
                        {"_id": ctx.guild.id},
                        {"$set": {str(channel.id): str(seconds)}},
                )
                
        except:
                await self.bot.mongo.db.shtimer.update_one(
                        {"_id": ctx.guild.id},
                        {"$set": {str(channel.id): str(seconds)}},
                )
        
        embed=discord.Embed(title="<:notify:965755380812611614> Ping Timer", description=f"**{seconds}** seconds ping timer has been set for <#{channel.id}>", color=0x36393F)
        await ctx.send(embed=embed) 
        
    @checks.has_started()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @timer.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def delete(self, ctx: commands.Context, channel: discord.TextChannel=None):
                
        if channel == None:
                return
        
        await self.bot.mongo.db.shtimer.delete_one(
                {"_id": ctx.guild.id},
                {"$set": {str(channel.id): str(seconds)}},
        )
        
        embed=discord.Embed(title="<:notify:965755380812611614> Ping Timer", description=f"Deleted ping timer for <#{channel.id}>", color=0x36393F)
        await ctx.send(embed=embed)
        
    @checks.has_started()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.hybrid_group(invoke_without_command=True, case_insensitive=True, slash_command=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def whitelist(self, ctx: commands.Context, channels: commands.Greedy[discord.TextChannel]):

        if len(channels) == 0:
            return await ctx.send("Please specify channels to whitelist collect pings.")

        await self.bot.mongo.update_guild(
            ctx.guild, {"$set": {"ping_channels": [x.id for x in channels]}}
        )
        
        await ctx.send("Now whitelisting collect pings in " + ", ".join(x.mention for x in channels))
    
    @checks.has_started()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @whitelist.command(slash_command=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def specialized(self, ctx, channels: commands.Greedy[discord.TextChannel]):
      """Whitelist specialized pings in certain channels"""

      await self.bot.mongo.update_guild(
            ctx.guild, {"$set": {"specialized": [x.id for x in channels]}}
        )

      embed=discord.Embed(title=":dizzy: Specialized Whitelist", description=f"Now whitelisting Specialized Pings in " + ", ".join(x.mention for x in channels), color=0x36393F)
      embed.set_thumbnail(url=ctx.guild.icon.url)
      await ctx.send(embed=embed)
    
    @checks.has_started()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @whitelist.command(slash_command=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def shiny(self, ctx, channels: commands.Greedy[discord.TextChannel]):
      """Whitelist shiny hunt in certain channels"""

      await self.bot.mongo.update_guild(
            ctx.guild, {"$set": {"sh_channels": [x.id for x in channels]}}
        )

      embed=discord.Embed(title=":sparkles: Shiny Whitelist", description=f"Now whitelisting Shiny Pings in " + ", ".join(x.mention for x in channels), color=0x36393F)
      embed.set_thumbnail(url=ctx.guild.icon.url)
      await ctx.send(embed=embed)

    @checks.has_started()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @whitelist.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def all(self, ctx: commands.Context):
        """Reset channels whitelist"""

        await ctx.send(f"All channels have been whitelisted.")

        await self.bot.mongo.update_guild(ctx.guild, {"$set": {"ping_channels": []}})

        await self.bot.mongo.update_guild(ctx.guild, {"$set": {"sh_channels": []}})

    @checks.has_started()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @whitelist.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def reset(self, ctx: commands.Context):
        """Clears all channels whitelist"""

        embed=discord.Embed(title="Whitelist Reset", description=f"All whitelisted channels have been cleared", color=0x36393F)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)

        await self.bot.mongo.update_guild(ctx.guild, {"$set": {"ping_channels": [877637271929647125]}})

        await self.bot.mongo.update_guild(ctx.guild, {"$set": {"sh_channels": [877637271929647125]}})
        
        await self.bot.mongo.update_guild(ctx.guild, {"$set": {"specialized": [877637271929647125]}})
  
    @checks.has_started()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @whitelist.command(slash_command=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def collect(self, ctx, channels: commands.Greedy[discord.TextChannel]):
        """Whitelist collecting list in certain channels"""

        if len(channels) == 0:
            return await ctx.send("Please specify channels to whitelist collect pings")

        await self.bot.mongo.update_guild(
            ctx.guild, {"$set": {"ping_channels": [x.id for x in channels]}}
        )

        embed=discord.Embed(title="<:pokeball:936773252913700894> Collect Whitelist", description=f"Now whitelisting Collect Pings in " + ", ".join(x.mention for x in channels), color=0x36393F)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)
        
    @checks.has_started()
    @commands.hybrid_group(aliases=("cl",), invoke_without_command=True, slash_command=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def collectlist(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        result = await self.bot.mongo.db.collector.find_one({"_id": member.id})
        
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
            await ctx.send("No pokémon or regions found.")
        

        
    @checks.has_started()
    @commands.hybrid_command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def serverlist(self, ctx):
        """Adds a server to your pinging list"""
        result = await self.bot.mongo.db.collector.find_one(
            {"_id": ctx.author.id}
        )

        async def get_guild(result):
            for key in result:
                try:
                    guild = self.bot.get_guild(int(key))
                    if guild:
                        yield guild
                except:
                    pass

        guilds = get_guild(result)
        
        pages = ViewMenuPages(
            source=AsyncEmbedListPageSource(
                guilds,
                title=f"{ctx.author}'s Server Pinging List",
                format_item=lambda x: f"{x}",
            )
        )

        try:
            await pages.start(ctx)
        except IndexError:
            embed=discord.Embed(title="Collector Server List", description="None", color=0x36393F)
            await ctx.send(embed=embed)
                
    @checks.has_started()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @collectlist.command(slash_command=True)
    async def view(self, ctx, *, member: discord.Member = None):

        """Allows members to keep track of the collectors for a pokémon or region"""
      
        if member is None:
            member = ctx.author

        result = await self.bot.mongo.db.collector.find_one({"_id": member.id})

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
            await ctx.send("No pokémon or regions found.")
        
    @checks.has_started()
    @collectlist.command(slash_command=True, brief="Adds a pokémon species to your collecting list.")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def add(self, ctx, *, pokemon: SpeciesConverter):
        
        """
        Usage: a!collectlist add <pokémon>
        Description: Adds a pokémon species or region to your collecting list.
        Category: Collectlist
        """

        result = await self.bot.mongo.db.collector.update_one(
            {"_id": ctx.author.id},
            {"$set": {str(pokemon.id): True}},
            upsert=True
        )

        if result.upserted_id or result.modified_count > 0:
            embed=discord.Embed(title="Collector", description=f"Added **{pokemon}** to your collecting list", color=0x36393F)
            embed.set_thumbnail(url=pokemon.image_url)
            
            await ctx.send(
                embed=embed
            )
        
        else:
            embed=discord.Embed(title="Collector", description=f"**{pokemon}** is already on your collecting list", color=0x36393F)
            embed.set_thumbnail(url=pokemon.image_url)
            
            await ctx.send(
                embed=embed, ephemeral=True #Returns ephemeral message if this command was invoked by slash.
            )
        
    @add.autocomplete('pokemon')
    async def add_autocomplete(self, interaction: discord.Interaction, current: str) -> List[discord.app_commands.Choice[str]]:
        matches = interaction.client.data.closest_species_by_name(current)
        
        if current is None:
            return
        
        return [
                discord.app_commands.Choice(name=match, value=match) for match in matches
        ]

    @checks.has_started()
    @collectlist.command(slash_command=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def multiadd(self, ctx, *, pokemons):
        """Adds a multiple pokémon species or region to your collecting list"""
        
        myList = []
        for i in pokemons.split(', '):
                species = self.bot.data.species_by_name(i)
                
                result = await self.bot.mongo.db.collector.update_one(
                        {"_id": ctx.author.id},
                        {"$set": {str(species.id): True}},
                        upsert=True,
                )
                
                if result.upserted_id or result.modified_count > 0:
                        myList.append(i.capitalize())
                        
                else:
                        await ctx.send(f"**{species}** is already on your collecting list")

        embed1=discord.Embed(title="Collector", description=f"Added **{', '.join(myList)}** to your collecting list", color=0x36393F)

        return await ctx.send(embed=embed1)

    @checks.has_started()
    @collectlist.command(slash_command=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def multiremove(self, ctx, *, pokemons):
        """Remove multiple pokémon species or region from your collecting list"""
        
        myList = []
        for i in pokemons.split(', '):
                species = self.bot.data.species_by_name(i)
                
                result = await self.bot.mongo.db.collector.update_one(
                        {"_id": ctx.author.id},
                        {"$unset": {str(species.id): True}},
                        upsert=True,
                )
                
                if result.upserted_id or result.modified_count > 0:
                        myList.append(i.capitalize())
                        
                else:
                        await ctx.send(f"**{species}** is already on your collecting list")

        embed=discord.Embed(title="Collector", description=f"Removed **{', '.join(myList)}** from your collecting list.", color=0x36393F)

        return await ctx.send(embed=embed)

    @checks.has_started()
    @collectlist.command(slash_command=True)
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def remove(self, ctx, *, species: SpeciesConverter):
        """Remove a pokémon species or region from your collecting list"""

        result = await self.bot.mongo.db.collector.update_one(
            {"_id": ctx.author.id},
            {"$unset": {str(species.id): 1}},
        )

        if result.modified_count > 0:
            embed=discord.Embed(title="Collector", description=f"Removed {species} from your collecting list.", color=0x36393F)
            embed.set_thumbnail(url=species.image_url)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Collector", description=f"**{species}** is not in your collecting list.", color=0x36393F)
            embed.set_thumbnail(url=species.image_url)
            await ctx.send(embed=embed, ephemeral=True)
    

    @checks.has_started()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.hybrid_command(aliases = ["fr"])
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def forceremove(self, ctx, *, user: FetchUserConverter):
        """Allows moderators to remove a player from pinging list"""
        
        result = await ctx.confirm(f"Are you sure you want to remove **{user}** from the **{ctx.guild}** pinging list?")
        
        if result is None:
                return await ctx.send("Time's up. Aborted.")

        if result is False:
                return await ctx.send("Aborted.")

        result = await self.bot.mongo.db.collector.update_one(
            {"_id": user.id},
            {"$unset": {str(ctx.guild.id): 1}},
            upsert=True,
        )
        
        result = await self.bot.mongo.db.shinyhunt.update_one(
            {"_id": user.id},
            {"$unset": {str(ctx.guild.id): 1}},
            upsert=True,
        )

        if result.upserted_id or result.modified_count > 0:
            return await ctx.send(f"Removed **{user}** from the **{ctx.guild}** pinging list.")
        else:
            return await ctx.send(f"**{user}** is not on the **{ctx.guild}** pinging list!")

    @checks.has_started()
    @collectlist.command()
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def clear(self, ctx):
        """Clear your collecting list."""
    
        result = await ctx.confirm('Your about to **clear** your collectlist. Are you sure you want to continue?')
        
        if result is None:
                return await ctx.send("Time's up. Aborted.")

        if result is False:
                return await ctx.send("Aborted.")
                
        await self.bot.mongo.db.collector.delete_one({"_id": ctx.author.id})
        await ctx.send("Cleared your collecting list.")

    @checks.has_started()
    @collectlist.command(slash_command=True)
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def globalsearch(self, ctx, *, species: SpeciesConverter):
        """Lists the collectors of a pokémon species or regions"""

        users = self.bot.mongo.db.collector.find({str(species.id): True})
        pages = ViewMenuPages(
            source=AsyncEmbedListPageSource(
                users,
                title=f"All {species} Collectors using the bot",
                format_item=lambda x: f"<@{x['_id']}>",
            )
        )

        
        await pages.start(ctx)
        
    @checks.has_started()
    @collectlist.command(slash_command=True)
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def search(self, ctx, *, species: SpeciesConverter):
        """Lists the collectors of a pokémon species or regions in the server"""

        users = self.bot.mongo.db.collector.find({str(species.id): True, str(ctx.guild.id): True})
        pages = ViewMenuPages(
            source=AsyncEmbedListPageSource(
                users,
                title=f"{species} Collectors in this server",
                format_item=lambda x: f"<@{x['_id']}>",
            )
        )

        try:
            await pages.start(ctx)
        except IndexError:
            await ctx.send("No users found.")

    async def make_config_embed(self, ctx, guild, commands={}):
        
        try:
            guild = await ctx.bot.mongo.fetch_guild(ctx.guild)
            spawn_co = int(guild["spawn_count"])
        except:
            spawn_co = 1
            
        if spawn_co >= 750:
            percentage = 100
        else:
            x = spawn_co / 750
            percentage = int((x % 1) * 100 // 1)
        #file = make_card(ctx.guild, spawn_co, percentage, ctx.guild.icon.url)
        
        user_data = {  # Most likely coming from database or calculation
            "name": ctx.guild.name,  # The user's name
            "xp": spawn_co,
            "percentage": percentage,
        }

        background = Editor(Canvas((934, 282), "#8F9296"))
        
        profile_image = load_image(str(ctx.guild.icon.url))
        profile = Editor(profile_image).resize((190, 190)).circle_image()

        poppins = Font.poppins(size=30)

        background.rectangle((20, 20), 894, 242, "#2a2e35")
        background.paste(profile, (50, 50))
        background.ellipse((42, 42), width=206, height=206, outline="#43b581", stroke_width=10)
        background.rectangle((260, 180), width=630, height=40, fill="#484b4e", radius=20)
        background.bar(
            (260, 180),
            max_width=630,
            height=40,
            percentage=user_data["percentage"],
            fill="#00fa81",
            radius=20,
        )
        background.text((270, 120), user_data["name"], font=poppins, color="#FFFFFF")
        background.text(
            (870, 125),
            f"{user_data['xp']} / 750",
            font=poppins,
            color="#00fa81",
            align="right",
        )
        
        rank_level_texts = [
            Text("Used ", color="#00fa81", font=poppins),
            Text(f"{user_data['xp']}", color="#1EAAFF", font=poppins),
            Text("   Total ", color="#00fa81", font=poppins),
            Text(f"750", color="#1EAAFF", font=poppins),
        ]

        background.multicolor_text((850, 30), texts=rank_level_texts, align="right")
        file = discord.File(fp=background.image_bytes, filename="poketox.png")
        
        embed = discord.Embed(color=0x36393F)
        embed.title = f"Server Configuration"
        embed.set_thumbnail(url=ctx.guild.icon.url)
                            
        pingchannel = "\n".join(f"<#{x}>" for x in guild.ping_channels) or "All Channels"
        shinychannel = "\n".join(f"<#{x}>" for x in guild.sh_channels) or "All Channels"
        specialized = "\n".join(f"<#{x}>" for x in guild.specialized) or "All Channels"
                                
        if str(pingchannel) == "<#877637271929647125>":
                pingchannel = "None"
        
        if str(shinychannel) == "<#877637271929647125>":
                shinychannel = "None"
                
        if str(specialized) == "<#877637271929647125>":
                specialized = "None"
        
        embed.add_field(
            name=f"Collecting Channels {commands.get('whitelist_command', '')}",
            value=pingchannel,
            inline=True,
        )

        embed.add_field(
            name=f"Shiny Hunt Channels {commands.get('whitelist_command', '')}",
            value=shinychannel,
            inline=False,
        )
        
        embed.add_field(
            name=f"Specialized Pings Channels {commands.get('whitelist_command', '')}",
            value=specialized,
            inline=False,
        )
                            
        embed.set_image(url="attachment://poketox.png")
        
        await ctx.send(embed=embed, file=file)

    @checks.has_started()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.hybrid_command(aliases = ["config"], slash_command=True, brief="Shows server configuration")
    async def configuration(self, ctx: commands.Context):
        
        guild = await self.bot.mongo.fetch_guild(ctx.guild)

        embed = await self.make_config_embed(ctx, guild)

async def setup(bot):
    print("Loaded Collectors")
    await bot.add_cog(Collectors(bot))
