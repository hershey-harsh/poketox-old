import discord
from discord.ext import commands
from discord.ext.menus.views import ViewMenuPages
from helpers.converters import FetchUserConverter, SpeciesConverter
from helpers import checks
from helpers.pagination import AsyncEmbedListPageSource

seconds_90 = [850069549037912065, 853006222042333194, 853006257611079681, 853006603262623795, 953404627028701214, 953404651494068335]
seconds_120 = [937716757387444294]

allowed = [826928105922232350, 826935014049972265, 797151240173125662, 875526899386953779, 790788488983085056, 950522564751544330]

import random
import asyncio

async def collectping(self, ctx, species: SpeciesConverter):
        guild = await ctx.bot.mongo.fetch_guild(ctx.guild)
        if guild.ping_channels and ctx.channel.id not in guild.ping_channels:
            return

        users = self.bot.mongo.db.collector.find(
            {str(species.id): True, str(ctx.guild.id): True}
        )

        collector_pings = []
        async for user in users:
            collector_pings.append(f"<@{user['_id']}> ")
        if len(collector_pings) > 0:
            await ctx.send(
                f"**Pinging {species} Collectors** \n \n" + " ".join(collector_pings)
            )
        else:
            mess = await ctx.send(
                f"No one is collecting {species}"
            )
           
async def shinyping(self, ctx, species: SpeciesConverter):
        """Ping shiny hunters of a pokemon"""

        guild = await ctx.bot.mongo.fetch_guild(ctx.guild)
        if guild["sh_channels"] and ctx.channel.id not in guild["sh_channels"]:
            return

        users = self.bot.mongo.db.shinyhunt.find(
            {str(ctx.guild.id): True, 'shinyhunt': species.id}
        )

        shinyhunt_pings = []
        async for user in users:
            shinyhunt_pings.append(f"<@{user['_id']}> ")
        if len(shinyhunt_pings) > 0:
            await ctx.send(
                f"**Pinging {species} Shiny Hunters** \n \n" + " ".join(shinyhunt_pings)
            )
        
            if ctx.channel.id in seconds_90:
                        server_timer = 90  
                        
            if ctx.channel.id in seconds_120:
                        server_timer = 120  
            
            try:
                await asyncio.sleep(int(server_timer))
                embed=discord.Embed(description=f"Post-Tag timer has expired for {species}. You may catch it now", color=0x2F3136)
                await ctx.send(embed=embed)
            except:
                pass
            
        else:
            mess = await ctx.send(
                f"No one is shiny hunting {species}!"
            )

q = ["Pokétox is made by Future#9409", "Like the bot? Type a!invite", "Want to help? DM Future#0005", "Join the offical server! https://discord.gg/futureworld"]

x = "Future#0811 is the best :)"

pi = "**Pinging"

names = ["Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata", "Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu", "Sandshrew", "Sandslash", "Nidoran", "Nidorina", "Nidoqueen", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat", "Venomoth", "Diglett", "Dugtrio", "Meowth", "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine", "Poliwag", "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash", "Slowpoke", "Slowbro", "Magnemite", "Magneton", "Farfetch’d", "Doduo", "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute", "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela", "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu", "Starmie", "Mr. Mime", "Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir", "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon", "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Articuno", "Zapdos", "Moltres", "Dratini", "Dragonair", "Dragonite", "Mewtwo", "Mew", "Chikorita", "Bayleef", "Meganium", "Cyndaquil", "Quilava", "Typhlosion", "Totodile", "Croconaw", "Feraligatr", "Sentret", "Furret", "Hoothoot", "Noctowl", "Ledyba", "Ledian", "Spinarak", "Ariados", "Crobat", "Chinchou", "Lanturn", "Pichu", "Cleffa", "Igglybuff", "Togepi", "Togetic", "Natu", "Xatu", "Mareep", "Flaaffy", "Ampharos", "Bellossom", "Marill", "Azumarill", "Sudowoodo", "Politoed", "Hoppip", "Skiploom", "Jumpluff", "Aipom", "Sunkern", "Sunflora", "Yanma", "Wooper", "Quagsire", "Espeon", "Umbreon", "Murkrow", "Slowking", "Misdreavus", "Unown", "Wobbuffet", "Girafarig", "Pineco", "Forretress", "Dunsparce", "Gligar", "Steelix", "Snubbull", "Granbull", "Qwilfish", "Scizor", "Shuckle", "Heracross", "Sneasel", "Teddiursa", "Ursaring", "Slugma", "Magcargo", "Swinub", "Piloswine", "Corsola", "Remoraid", "Octillery", "Delibird", "Mantine", "Skarmory", "Houndour", "Houndoom", "Kingdra", "Phanpy", "Donphan", "Porygon2", "Stantler", "Smeargle", "Tyrogue", "Hitmontop", "Smoochum", "Elekid", "Magby", "Miltank", "Blissey", "Raikou", "Entei", "Suicune", "Larvitar", "Pupitar", "Tyranitar", "Lugia", "Ho-Oh", "Celebi", "Treecko", "Grovyle", "Sceptile", "Torchic", "Combusken", "Blaziken", "Mudkip", "Marshtomp", "Swampert", "Poochyena", "Mightyena", "Zigzagoon", "Linoone", "Wurmple", "Silcoon", "Beautifly", "Cascoon", "Dustox", "Lotad", "Lombre", "Ludicolo", "Seedot", "Nuzleaf", "Shiftry", "Taillow", "Swellow", "Wingull", "Pelipper", "Ralts", "Kirlia", "Gardevoir", "Surskit", "Masquerain", "Shroomish", "Breloom", "Slakoth", "Vigoroth", "Slaking", "Nincada", "Ninjask", "Shedinja", "Whismur", "Loudred", "Exploud", "Makuhita", "Hariyama", "Azurill", "Nosepass", "Skitty", "Delcatty", "Sableye", "Mawile", "Aron", "Lairon", "Aggron", "Meditite", "Medicham", "Electrike", "Manectric", "Plusle", "Minun", "Volbeat", "Illumise", "Roselia", "Gulpin", "Swalot", "Carvanha", "Sharpedo", "Wailmer", "Wailord", "Numel", "Camerupt", "Torkoal", "Spoink", "Grumpig", "Spinda", "Trapinch", "Vibrava", "Flygon", "Cacnea", "Cacturne", "Swablu", "Altaria", "Zangoose", "Seviper", "Lunatone", "Solrock", "Barboach", "Whiscash", "Corphish", "Crawdaunt", "Baltoy", "Claydol", "Lileep", "Cradily", "Anorith", "Armaldo", "Feebas", "Milotic", "Castform", "Kecleon", "Shuppet", "Banette", "Duskull", "Dusclops", "Tropius", "Chimecho", "Absol", "Wynaut", "Snorunt", "Glalie", "Spheal", "Sealeo", "Walrein", "Clamperl", "Huntail", "Gorebyss", "Relicanth", "Luvdisc", "Bagon", "Shelgon", "Salamence", "Beldum", "Metang", "Metagross", "Regirock", "Regice", "Registeel", "Latias", "Latios", "Kyogre", "Groudon", "Rayquaza", "Jirachi", "Deoxys", "Turtwig", "Grotle", "Torterra", "Chimchar", "Monferno", "Infernape", "Piplup", "Prinplup", "Empoleon", "Starly", "Staravia", "Staraptor", "Bidoof", "Bibarel", "Kricketot", "Kricketune", "Shinx", "Luxio", "Luxray", "Budew", "Roserade", "Cranidos", "Rampardos", "Shieldon", "Bastiodon", "Burmy", "Wormadam", "Mothim", "Combee", "Vespiquen", "Pachirisu", "Buizel", "Floatzel", "Cherubi", "Cherrim", "Shellos", "Gastrodon", "Ambipom", "Drifloon", "Drifblim", "Buneary", "Lopunny", "Mismagius", "Honchkrow", "Glameow", "Purugly", "Chingling", "Stunky", "Skuntank", "Bronzor", "Bronzong", "Bonsly", "Mime Jr.", "Happiny", "Chatot", "Spiritomb", "Gible", "Gabite", "Garchomp", "Munchlax", "Riolu", "Lucario", "Hippopotas", "Hippowdon", "Skorupi", "Drapion", "Croagunk", "Toxicroak", "Carnivine", "Finneon", "Lumineon", "Mantyke", "Snover", "Abomasnow", "Weavile", "Magnezone", "Lickilicky", "Rhyperior", "Tangrowth", "Electivire", "Magmortar", "Togekiss", "Yanmega", "Leafeon", "Glaceon", "Gliscor", "Mamoswine", "Porygon-Z", "Gallade", "Probopass", "Dusknoir", "Froslass", "Rotom", "Uxie", "Mesprit", "Azelf", "Dialga", "Palkia", "Heatran", "Regigigas", "Giratina", "Cresselia", "Phione", "Manaphy", "Darkrai", "Shaymin", "Arceus", "Victini", "Snivy", "Servine", "Serperior", "Tepig", "Pignite", "Emboar", "Oshawott", "Dewott", "Samurott", "Patrat", "Watchog", "Lillipup", "Herdier", "Stoutland", "Purrloin", "Liepard", "Pansage", "Simisage", "Pansear", "Simisear", "Panpour", "Simipour", "Munna", "Musharna", "Pidove", "Tranquill", "Unfezant", "Blitzle", "Zebstrika", "Roggenrola", "Boldore", "Gigalith", "Woobat", "Swoobat", "Drilbur", "Excadrill", "Audino", "Timburr", "Gurdurr", "Conkeldurr", "Tympole", "Palpitoad", "Seismitoad", "Throh", "Sawk", "Sewaddle", "Swadloon", "Leavanny", "Venipede", "Whirlipede", "Scolipede", "Cottonee", "Whimsicott", "Petilil", "Lilligant", "Basculin", "Sandile", "Krokorok", "Krookodile", "Darumaka", "Darmanitan", "Maractus", "Dwebble", "Crustle", "Scraggy", "Scrafty", "Sigilyph", "Yamask", "Cofagrigus", "Tirtouga", "Carracosta", "Archen", "Archeops", "Trubbish", "Garbodor", "Zorua", "Zoroark", "Minccino", "Cinccino", "Gothita", "Gothorita", "Gothitelle", "Solosis", "Duosion", "Reuniclus", "Ducklett", "Swanna", "Vanillite", "Vanillish", "Vanilluxe", "Deerling", "Sawsbuck", "Emolga", "Karrablast", "Escavalier", "Foongus", "Amoonguss", "Frillish", "Jellicent", "Alomomola", "Joltik", "Galvantula", "Ferroseed", "Ferrothorn", "Klink", "Klang", "Klinklang", "Tynamo", "Eelektrik", "Eelektross", "Elgyem", "Beheeyem", "Litwick", "Lampent", "Chandelure", "Axew", "Fraxure", "Haxorus", "Cubchoo", "Beartic", "Cryogonal", "Shelmet", "Accelgor", "Stunfisk", "Mienfoo", "Mienshao", "Druddigon", "Golett", "Golurk", "Pawniard", "Bisharp", "Bouffalant", "Rufflet", "Braviary", "Vullaby", "Mandibuzz", "Heatmor", "Durant", "Deino", "Zweilous", "Hydreigon", "Larvesta", "Volcarona", "Cobalion", "Terrakion", "Virizion", "Tornadus", "Thundurus", "Reshiram", "Zekrom", "Landorus", "Kyurem", "Keldeo", "Meloetta", "Genesect", "Chespin", "Quilladin", "Chesnaught", "Fennekin", "Braixen", "Delphox", "Froakie", "Frogadier", "Greninja", "Bunnelby", "Diggersby", "Fletchling", "Fletchinder", "Talonflame", "Scatterbug", "Spewpa", "Vivillon", "Litleo", "Pyroar", "Flabebe", "Floette", "Florges", "Skiddo", "Gogoat", "Pancham", "Pangoro", "Furfrou", "Espurr", "Meowstic", "Honedge", "Doublade", "Aegislash", "Spritzee", "Aromatisse", "Swirlix", "Slurpuff", "Inkay", "Malamar", "Binacle", "Barbaracle", "Skrelp", "Dragalge", "Clauncher", "Clawitzer", "Helioptile", "Heliolisk", "Tyrunt", "Tyrantrum", "Amaura", "Aurorus", "Sylveon", "Hawlucha", "Dedenne", "Carbink", "Goomy", "Sliggoo", "Goodra", "Klefki", "Phantump", "Trevenant", "Pumpkaboo", "Gourgeist", "Bergmite", "Avalugg", "Noibat", "Noivern", "Xerneas", "Yveltal", "Zygarde", "Diancie", "Hoopa", "Volcanion", "Rowlet", "Dartrix", "Decidueye", "Litten", "Torracat", "Incineroar", "Popplio", "Brionne", "Primarina", "Pikipek", "Trumbeak", "Toucannon", "Yungoos", "Gumshoos", "Grubbin", "Charjabug", "Vikavolt", "Crabrawler", "Crabominable", "Oricorio", "Cutiefly", "Ribombee", "Rockruff", "Lycanroc", "Wishiwashi", "Mareanie", "Toxapex", "Mudbray", "Mudsdale", "Dewpider", "Araquanid", "Fomantis", "Lurantis", "Morelull", "Shiinotic", "Salandit", "Salazzle", "Stufful", "Bewear", "Bounsweet", "Steenee", "Tsareena", "Comfey", "Oranguru", "Passimian", "Wimpod", "Golisopod", "Sandygast", "Palossand", "Pyukumuku", "Type: Null", "Silvally", "Minior", "Komala", "Turtonator", "Togedemaru", "Mimikyu", "Bruxish", "Drampa", "Dhelmise", "Jangmo-o", "Hakamo-o", "Kommo-o", "Alolan Rattata", "Alolan Raticate", "Alolan Raichu", "Alolan Sandshrew", "Alolan Sandslash", "Alolan Vulpix", "Alolan Ninetales", "Alolan Diglett", "Alolan Dugtrio", "Alolan Meowth", "Alolan Persian", "Alolan Geodude", "Alolan Graveler", "Alolan Golem", "Alolan Grimer", "Alolan Muk", "Alolan Exeggutor", "Alolan Marowak", "Tapu Koko", "Tapu Lele", "Tapu Bulu", "Tapu Fini", "Cosmog", "Cosmoem", "Solgaleo", "Lunala", "Nihilego", "Buzzwole", "Pheromosa", "Xurkitree", "Celesteela", "Kartana", "Guzzlord", "Necrozma", "Magearna", "Marshadow", "Poipole", "Naganadel", "Stakataka", "Blacephalon", "Zeraora", "Meltan", "Melmetal",  "Grookey", "Thwackey", "Rillaboom", "Scorbunny", "Raboot", "Cinderace", "Sobble", "Drizzile", "Inteleon", "Skwovet", "Greedent", "Rookidee", "Corvisquire", "Corviknight", "Blipbug", "Dottler", "Orbeetle", "Nickit", "Thievul", "Gossifleur", "Eldegoss", "Wooloo", "Dubwool", "Chewtle", "Drednaw", "Yamper", "Boltund", "Rolycoly", "Carkol", "Coalossal", "Applin", "Flapple", "Appletun", "Silicobra", "Sandaconda", "Cramorant", "Arrokuda", "Barraskewda", "Toxel", "Toxtricity", "Sizzlipede", "Centiskorch", "Clobbopus", "Grapploct", "Sinistea", "Polteageist", "Hatenna", "Hattrem", "Hatterene", "Impidimp", "Morgrem", "Grimmsnarl", "Galarian Zigzagoon", "Galarian Linoone", "Obstagoon", "Galarian Meowth", "Perrserker", "Galarian Ponyta", "Galarian Rapidash", "Galarian Slowpoke", "Galarian Slowbro", "Galarian Slowking", "Galarian Corsola", "Cursola", "Galarian Farfetch’d", "Sirfetch'd", "Galarian Weezing", "Galarian Mr. Mime", "Mr. Rime", "Galarian Darumaka", "Galarian Darmanitan", "Galarian Yamask", "Runerigus", "Galarian Stunfisk", "Milcery", "Alcremie", "Falinks", "Pincurchin", "Snom", "Frosmoth", "Stonjourner", "Eiscue", "Indeedee", "Morpeko", "Cufant", "Copperajah", "Dracozolt", "Arctozolt", "Dracovish", "Arctovish", "Duraludon", "Dreepy", "Drakloak", "Dragapult", "Zacian", "Zamazenta", "Eternatus", "Kubfu", "Urshifu", "Zarude", "Regieleki", "Regidrago", "Glastrier", "Spectrier", "Calyrex", "Galarian Articuno", "Galarian Zapdos", "Galarian Moltres"]

import urllib

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
    @commands.group(invoke_without_command=True, case_insensitive=True, slash_command=True)
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
    async def shiny(self, ctx, channels: commands.Greedy[discord.TextChannel]):
      """Whitelist Shiny Hunt in certain channels"""

      await self.bot.mongo.update_guild(
            ctx.guild, {"$set": {"sh_channels": [x.id for x in channels]}}
        )

      await ctx.send("Now whitelisting Shiny pings in " + ", ".join(x.mention for x in channels))  

    @checks.has_started()
    @commands.has_permissions(manage_messages=True)
    @whitelist.command()
    async def all(self, ctx: commands.Context):
        """Reset channel whitelist."""

        await ctx.send(f"All channels have been whitelisted.")

        await self.bot.mongo.update_guild(ctx.guild, {"$set": {"ping_channels": []}})

        await self.bot.mongo.update_guild(ctx.guild, {"$set": {"sh_channels": []}})

    @checks.has_started()
    @commands.has_permissions(manage_messages=True)
    @whitelist.command()
    async def reset(self, ctx: commands.Context):
        """Clears all channels whitelist."""

        await ctx.send(f"All channels have been cleared.")

        await self.bot.mongo.update_guild(ctx.guild, {"$set": {"ping_channels": [877637271929647125]}})

        await self.bot.mongo.update_guild(ctx.guild, {"$set": {"sh_channels": [877637271929647125]}})
  
    @checks.has_started()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @whitelist.command(slash_command=True)
    async def collect(self, ctx, channels: commands.Greedy[discord.TextChannel]):
        """Whitelist Collecting List in certain channels"""

        if len(channels) == 0:
            return await ctx.send("Please specify channels to whitelist collect pings")

        await self.bot.mongo.update_guild(
            ctx.guild, {"$set": {"ping_channels": [x.id for x in channels]}}
        )
        await ctx.send("Now whitelisting collect pings in " + ", ".join(x.mention for x in channels))
        
    @checks.has_started()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.group(aliases=("cl",), invoke_without_command=True, slash_command=True)
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
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(slash_command=True)
    async def enable(self, ctx, guildid=None):
        """Adds a server to your pinging list"""
        guildid = guildid
        if guildid == None:
          guildid = ctx.guild.id
        
        result = await self.bot.mongo.db.collector.update_one(
            {"_id": ctx.author.id},
            {"$set": {str(ctx.guild.id): True}},
            upsert=True,
        )
        
        result = await self.bot.mongo.db.shinyhunt.update_one(
            {"_id": ctx.author.id},
            {"$set": {str(ctx.guild.id): True}},
            upsert=True,
        )

        if result.upserted_id or result.modified_count > 0:
            embed=discord.Embed(title="Collector", description=f"You will get pinged when your shiny hunt spawns or what your collecting in **{ctx.guild}**", color=0x36393F)
            embed.set_footer(text="Tip: You can always turn this feature of with a!disable")
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Collector", description=f"This feature is already enabled in **{ctx.guild}**! **Tip:** You can always turn this feature of with `a!disable`", color=0x36393F)
            embed.set_footer(text=x)
            await ctx.send(embed=embed)
       
    @checks.has_started()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(slash_command=True)
    async def disable(self, ctx):
        """Adds a server to your pinging list"""
        result = await self.bot.mongo.db.collector.update_one(
            {"_id": ctx.author.id},
            {"$unset": {str(ctx.guild.id): 1}},
            upsert=True,
        )
        
        result = await self.bot.mongo.db.shinyhunt.update_one(
            {"_id": ctx.author.id},
            {"$unset": {str(ctx.guild.id): 1}},
            upsert=True,
        )

        if result.upserted_id or result.modified_count > 0:
            embed=discord.Embed(title="Ping", description=f"You will not get pinged when your shiny hunt or what your collecting spawns in **{ctx.guild}**", color=0x36393F)
            embed.set_footer(text="Tip: You can always turn this feature on with a!enable")
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Ping", description=f"This feature is already disabled in **{ctx.guild}**!", color=0x36393F)
            embed.set_footer(text="Tip: You can always turn this feature on with a!enable")
            await ctx.send(embed=embed)
        
    @checks.has_started()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(slash_command=True)
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
        
        pages = menus.MenuPages(
            source=AsyncListPageSource(
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

        """Allows members to keep track of the collectors for a pokémon or region
        If no subcommand is called, lists the pokémon or regions collected by you or someone else.
        """
      
        if member is None:
            member = ctx.author

        result = await self.bot.mongo.db.collector.find_one({"_id": member.id})

        pages = menus.MenuPages(
            source=AsyncListPageSource(
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
    @commands.cooldown(1, 3, commands.BucketType.user)
    @collectlist.command(slash_command=True)
    async def add(self, ctx, *, species: SpeciesConverter):
        """Adds a pokémon species or region to your collecting list"""

        result = await self.bot.mongo.db.collector.update_one(
            {"_id": ctx.author.id},
            {"$set": {str(species.id): True}},
            upsert=True,
        )

        if result.upserted_id or result.modified_count > 0:
            embed1=discord.Embed(title="Collector", description=f"Added **{species}** to your collecting list", color=0x36393F)
            embed1.set_thumbnail(url=species.image_url)

            return await ctx.send(embed=embed1)
        else:

            embed2=discord.Embed(title="Collector", description=f"**{species}** is already on your collecting list", color=0x36393F)
            embed2.set_thumbnail(url=species.image_url)
            return await ctx.send(embed=embed2, ephemeral=True)

    @checks.has_started()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @collectlist.command(slash_command=True)
    async def remove(self, ctx, *, species: SpeciesConverter):
        """Remove a pokémon species or region from your collecting list"""

        result = await self.bot.mongo.db.collector.update_one(
            {"_id": ctx.author.id},
            {"$unset": {str(species.id): 1}},
        )

        if result.modified_count > 0:
            embed=discord.Embed(title="Collector", description=f"{species} has been removed from your collecting list.", color=0x36393F)
            embed.set_thumbnail(url=species.image_url)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Collector", description=f"**{species}** is not in your collecting list.", color=0x36393F)
            embed.set_thumbnail(url=species.image_url)
            await ctx.send(embed=embed, ephemeral=True)
    

    @checks.has_started()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases = ["fr"], slash_command=True)
    async def forceremove(self, ctx, *, user: FetchUserConverter):
        """Allows moderators to remove a player from pinging list"""

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
    @commands.cooldown(1, 3, commands.BucketType.user)
    @collectlist.command(slash_command=True)
    async def clear(self, ctx):
        """Clear your collecting list."""

        await self.bot.mongo.db.collector.delete_one({"_id": ctx.author.id})
        await ctx.send("Cleared your collecting list.")

    @checks.has_started()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @collectlist.command(slash_command=True)
    async def globalsearch(self, ctx, *, species: SpeciesConverter):
        """Lists the collectors of a pokémon species or regions"""

        users = self.bot.mongo.db.collector.find({str(species.id): True})
        pages = menus.MenuPages(
            source=AsyncListPageSource(
                users,
                title=f"All {species} Collectors using the bot",
                color=0x36393F,
                format_item=lambda x: f"<@{x['_id']}>",
            )
        )

        
        await pages.start(ctx)
        
    @checks.has_started()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @collectlist.command(slash_command=True)
    async def search(self, ctx, *, species: SpeciesConverter):
        """Lists the collectors of a pokémon species or regions in the server"""

        users = self.bot.mongo.db.collector.find({str(species.id): True, str(ctx.guild.id): True})
        pages = menus.MenuPages(
            source=AsyncListPageSource(
                users,
                title=f"{species} Collectors in this server",
                color=0x36393F,
                format_item=lambda x: f"<@{x['_id']}>",
            )
        )

        try:
            await pages.start(ctx)
        except IndexError:
            await ctx.send("No users found.")

    def make_config_embed(self, ctx, guild, commands={}):
        embed = discord.Embed(color=0x36393F)
        embed.title = f"Server Configuration"
        embed.set_thumbnail(url=ctx.guild.icon.url)

        embed.add_field(
            name=f"Pinging Channels {commands.get('whitelist_command', '')}",
            value="\n".join(f"<#{x}>" for x in guild.ping_channels) or "All Channels",
            inline=True,
        )

        embed.add_field(
            name=f"Shiny Hunt Channels {commands.get('whitelist_command', '')}",
            value="\n".join(f"<#{x}>" for x in guild.sh_channels) or "All Channels",
            inline=False,
        )
        
        return embed

    @checks.has_started()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(aliases = ["config"], slash_command=True)
    async def configuration(self, ctx: commands.Context):
        
        guild = await self.bot.mongo.fetch_guild(ctx.guild)

        embed = self.make_config_embed(ctx, guild)
        
        await ctx.send(embed=embed)
        
    @commands.Cog.listener()
    async def on_guild_leave(self, guild):
      del db[db[str(guild.id)]]
      


def setup(bot):
    print("Loaded Collectors")
    bot.add_cog(Collectors(bot))
