import discord
from discord.ext import commands
import random
import time
import math
import config

import asyncio
import requests
import json
import random
import asyncio
import datetime
from name import solve  
import discord
from data import models
from discord.ext import commands, menus
from helpers.converters import FetchUserConverter, SpeciesConverter
from helpers.pagination import AsyncListPageSource
from helpers import checks
import asyncio
from replit import db
import discord,random,os
import dbl
from discord.ext import commands

class comands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dblpy = dbl.DBLClient(self.bot, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijg3NTUyNjg5OTM4Njk1Mzc3OSIsImJvdCI6dHJ1ZSwiaWF0IjoxNjUwNDE0MjMzfQ.7aZSEjaVH-lH-KtBe_Q2pmGA-wnbyLLbODxEhcfghAE")
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.embeds and message.channel.id == 966129589275471902:
            voter_id = message.embeds[0].footer.value
            
    @checks.has_started()
    @commands.command(brief="Suggest new features")
    async def suggest(self, ctx, *, args):
      chan = self.bot.get_channel(939162941536735292)
      
      embed=discord.Embed(title="💡 Suggestion", color=0x5865F2)
      embed.add_field(name="Server", value=f"{ctx.guild} (*{ctx.guild.id}*)", inline=True)
      embed.add_field(name="User", value=f"{ctx.author.mention} (*{ctx.author.id}*)", inline=True)
      embed.add_field(name="Suggestion", value=f'> "{args}"', inline=False)
      
      await chan.send(embed=embed) 
        
      embed=discord.Embed(title="Suggestion Sent", color=0x2F3136)
        
    @checks.has_started()
    @commands.is_owner()
    @commands.command()
    async def dm(ctx, user: discord.User, *, message=None):
        await user.send(message)
        await ctx.send("Sent Message")
          
    @checks.has_started()
    @commands.command()
    async def botstats(self, ctx):
        """Pokétox stats"""

        embed = discord.Embed(color=0x2F3136, title = f"Pokétox Statistics")
        embed.add_field(
            name = "Total servers", 
            value = f"{len(self.bot.guilds)}", 
            inline = False
        )

        total_members = 0
        for guild in self.bot.guilds:
            total_members += guild.member_count

        embed.add_field(
            name = "Total Members", 
            value = f"{total_members}",
            inline = False
        )

        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/875526899386953779/d46976087eef1662db19c8272ebb57e4.png?size=1024")
        await ctx.send(embed = embed)
        
    @checks.has_started()
    @commands.command()
    async def vote(self, ctx):
        """Vote for the Pokétox"""

        embed = discord.Embed(color=0x2F3136, title = f"Vote for the bot below")
        embed.add_field(
            name = "Vote for the bot", 
            value = f"[Top.gg bot voting](https://top.gg/bot/875526899386953779/vote)", 
            inline = False
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/875526899386953779/d46976087eef1662db19c8272ebb57e4.png?size=1024")
        await ctx.send(embed=embed)
        
    @checks.has_started()
    @commands.command(aliases=("sr",))
    async def shinyrate(self, ctx, streak=1):
        """Check the shinyrate for a specific shiny hunt streak"""
        
        wsc = f'{4096/(1+math.log(1+streak/30)): .3f}'
        wsc = "{:,}".format(int(float(wsc)))

        embed = discord.Embed(color=0x2F3136, title = f"Shiny Rate", description=f"Shiny Rate for {streak} shiny hunt streak")
        embed.add_field(
            name = "Without shiny charm", 
            value = f"1 in {wsc}", 
            inline = False
        )
        
        wsc = f'{3413.33/(1+math.log(1+streak/30)): .3f}'
        wsc = "{:,}".format(int(float(wsc)))
        
        embed.add_field(
            name = "With shiny charm", 
            value = f"1 in {wsc}",
            inline = False
        )
        await ctx.send(embed = embed)
        
    @checks.has_started()
    @commands.command()
    async def spawnrate(self, ctx, pokemon):
        
        pokemon = pokemon.capitalize()
        
        zero_set = ["Galarian Articuno", "Galarian Zapdos", "Galarian Moltres"]
        first_set = ["Nihilego", "Buzzwole", "Pheromosa", "Xurkitree", "Celesteela", "Kartana", "Guzzlord", "Poipole", "Naganadel", "Stakataka", "Blacephalon"]
        second_set = ["Articuno", "Zapdos", "Moltres", "Mewtwo", "Raikou", "Entei", "Suicune", "Lugia", "Ho-Oh", "Regirock", "Regice", "Registeel", "Latias", "Latios", "Kyogre", "Groudon", "Rayquaza", "Uxie", "Mesprit", "Azelf", "Dialga", "Palkia", "Heatran", "Regigigas", "Giratina", "Cresselia", "Cobalion", "Terrakion", "Virizion", "Tornadus", "Thundurus", "Reshiram", "Zekrom", "Landorus", "Kyurem", "Xerneas", "Yveltal", "Zygarde", "Type: Null", "Silvally", "Tapu Koko", "Tapu Lele", "Tapu Bulu", "Tapu Fini", "Cosmog", "Cosmoem", "Solgaleo", "Lunala", "Necrozma", "Mr. Rime", "Zacian", "Zamazenta", "Eternatus", "Kubfu", "Urshifu", "Regieleki", "Regidrago", "Glastrier", "Spectrier", "Calyrex", "Alolan Golem", "10% Zygarde", "Complete Zygarde", "Galarian Slowking", "Rapid Strike Urshifu"]
        third_set = ["Mew", "Celebi", "Jirachi", "Deoxys", "Phione", "Manaphy", "Darkrai", "Shaymin", "Arceus", "Victini", "Keldeo", "Meloetta", "Genesect", "Diancie", "Hoopa", "Volcanion", "Magearna", "Marshadow", "Zeraora", "Meltan", "Melmetal", "Obstagoon", "Perrserker", "Cursola", "Sirfetch'd", "Runerigus", "Zarude", "Attack Deoxys", "Defense Deoxys", "Speed Deoxys", "Alolan Raticate", "Alolan Sandslash", "Alolan Ninetales", "Alolan Dugtrio", "Alolan Persian", "Alolan Graveler", "Alolan Muk", "Alolan Exeggutor", "Alolan Marowak", "Galarian Rapidash", "Galarian Slowbro", "Galarian Weezing", "Galarian Mr. Mime", "Galarian Zigzagoon", "Galarian Darumaka", "Galarian Stunfisk"]
        four_set = ["Alolan Rattata", "Alolan Raichu", "Alolan Sandshrew", "Alolan Vulpix", "Alolan Diglett", "Alolan Meowth", "Alolan Geodude", "Alolan Grimer", "Galarian Meowth", "Galarian Ponyta", "Galarian Slowpoke", "Galarian Farfetch'd", "Galarian Corsola", "Galarian Linoone", "Galarian Darmanitan", "Galarian Yamask"]
        fifth_set = ["Dragonite", "Tyranitar", "Salamence", "Metagross", "Garchomp", "Hydreigon", "Goodra", "Kommo-o"]
        sixth_set = ["Venusaur", "Charizard", "Blastoise", "Butterfree", "Beedrill", "Pidgeot", "Fearow", "Arbok", "Raichu", "Sandslash", "Nidoqueen", "Nidoking", "Clefable", "Ninetales", "Wigglytuff", "Vileplume", "Parasect", "Venomoth", "Dugtrio", "Persian", "Golduck", "Primeape", "Arcanine", "Poliwrath", "Alakazam", "Machamp", "Victreebel", "Tentacruel", "Golem", "Rapidash", "Slowbro", "Farfetch'd", "Dodrio", "Dewgong", "Muk", "Cloyster", "Gengar", "Hypno", "Kingler", "Electrode", "Exeggutor", "Marowak", "Hitmonlee", "Hitmonchan", "Weezing", "Kangaskhan", "Seaking", "Starmie", "Mr. Mime", "Jynx", "Pinsir", "Tauros", "Gyarados", "Lapras", "Ditto", "Vaporeon", "Jolteon", "Flareon", "Omastar", "Kabutops", "Aerodactyl", "Snorlax", "Meganium", "Typhlosion", "Feraligatr", "Furret", "Noctowl", "Ledian", "Ariados", "Crobat", "Lanturn", "Pichu", "Cleffa", "Igglybuff", "Xatu", "Ampharos", "Bellossom", "Azumarill", "Sudowoodo", "Politoed", "Jumpluff", "Sunflora", "Quagsire", "Espeon", "Umbreon", "Slowking", "Unown", "Wobbuffet", "Girafarig", "Forretress", "Dunsparce", "Steelix", "Granbull", "Qwilfish", "Scizor", "Shuckle", "Heracross", "Ursaring", "Magcargo", "Corsola", "Octillery", "Delibird", "Mantine", "Skarmory", "Houndoom", "Kingdra", "Donphan", "Stantler", "Smeargle", "Hitmontop", "Smoochum", "Elekid", "Magby", "Miltank", "Blissey", "Sceptile", "Blaziken", "Swampert", "Mightyena", "Linoone", "Beautifly", "Dustox", "Ludicolo", "Shiftry", "Swellow", "Pelipper", "Gardevoir", "Masquerain", "Breloom", "Slaking", "Ninjask", "Shedinja", "Exploud", "Hariyama", "Azurill", "Delcatty", "Sableye", "Mawile", "Aggron", "Medicham", "Manectric", "Plusle", "Minun", "Volbeat", "Illumise", "Swalot", "Sharpedo", "Wailord", "Camerupt", "Torkoal", "Grumpig", "Spinda", "Flygon", "Cacturne", "Altaria", "Zangoose", "Seviper", "Lunatone", "Solrock", "Whiscash", "Crawdaunt", "Claydol", "Cradily", "Armaldo", "Milotic", "Castform", "Kecleon", "Banette", "Tropius", "Chimecho", "Absol", "Wynaut", "Glalie", "Walrein", "Huntail", "Gorebyss", "Relicanth", "Luvdisc", "Torterra", "Infernape", "Empoleon", "Staraptor", "Bibarel", "Kricketune", "Luxray", "Budew", "Roserade", "Rampardos", "Bastiodon", "Wormadam", "Mothim", "Vespiquen", "Pachirisu", "Floatzel", "Cherrim", "Gastrodon", "Ambipom", "Drifblim", "Lopunny", "Mismagius", "Honchkrow", "Purugly", "Chingling", "Skuntank", "Bronzong", "Bonsly", "Mime Jr.", "Happiny", "Chatot", "Spiritomb", "Munchlax", "Lucario", "Hippowdon", "Drapion", "Toxicroak", "Carnivine", "Lumineon", "Mantyke", "Abomasnow", "Weavile", "Magnezone", "Lickilicky", "Rhyperior", "Tangrowth", "Electivire", "Magmortar", "Togekiss", "Yanmega", "Leafeon", "Glaceon", "Gliscor", "Mamoswine", "Porygon-Z", "Gallade", "Probopass", "Dusknoir", "Froslass", "Rotom", "Serperior", "Emboar", "Samurott", "Watchog", "Stoutland", "Liepard", "Simisage", "Simisear", "Simipour", "Musharna", "Unfezant", "Zebstrika", "Gigalith", "Swoobat", "Excadrill", "Audino", "Conkeldurr", "Seismitoad", "Throh", "Sawk", "Leavanny", "Scolipede", "Whimsicott", "Lilligant", "Basculin", "Krookodile", "Darmanitan", "Maractus", "Crustle", "Scrafty", "Sigilyph", "Cofagrigus", "Carracosta", "Archeops", "Garbodor", "Zoroark", "Cinccino", "Gothitelle", "Reuniclus", "Swanna", "Vanilluxe", "Sawsbuck", "Emolga", "Escavalier", "Amoonguss", "Jellicent", "Alomomola", "Galvantula", "Ferrothorn", "Klinklang", "Eelektross", "Beheeyem", "Chandelure", "Haxorus", "Beartic", "Cryogonal", "Accelgor", "Stunfisk", "Mienshao", "Druddigon", "Golurk", "Bisharp", "Bouffalant", "Braviary", "Mandibuzz", "Heatmor", "Durant", "Volcarona", "Chesnaught", "Delphox", "Greninja", "Diggersby", "Talonflame", "Vivillon", "Pyroar", "Florges", "Gogoat", "Pangoro", "Furfrou", "Meowstic", "Aegislash", "Aromatisse", "Slurpuff", "Malamar", "Barbaracle", "Dragalge", "Clawitzer", "Heliolisk", "Tyrantrum", "Aurorus", "Sylveon", "Hawlucha", "Dedenne", "Carbink", "Klefki", "Trevenant", "Gourgeist", "Avalugg", "Noivern", "Decidueye", "Incineroar", "Primarina", "Toucannon", "Gumshoos", "Vikavolt", "Crabominable", "Oricorio", "Ribombee", "Lycanroc", "Wishiwashi", "Toxapex", "Mudsdale", "Araquanid", "Lurantis", "Shiinotic", "Salazzle", "Bewear", "Tsareena", "Comfey", "Oranguru", "Passimian", "Golisopod", "Palossand", "Pyukumuku", "Minior", "Komala", "Turtonator", "Togedemaru", "Mimikyu", "Bruxish", "Drampa", "Dhelmise", "Rillaboom", "Cinderace", "Inteleon", "Greedent", "Corviknight", "Orbeetle", "Thievul", "Eldegoss", "Dubwool", "Drednaw", "Boltund", "Coalossal", "Flapple", "Appletun", "Sandaconda", "Cramorant", "Barraskewda", "Toxtricity", "Centiskorch", "Grapploct", "Polteageist", "Hatterene", "Grimmsnarl", "Alcremie", "Falinks", "Pincurchin", "Frosmoth", "Stonjourner", "Eiscue", "Indeedee", "Morpeko", "Copperajah", "Dracozolt", "Arctozolt", "Dracovish", "Arctovish", "Duraludon", "Dragapult", "Sandy Wormadam", "Trash Wormadam", "Sunny Castform", "Rainy Castform", "Snowy Castform", "Blue-Striped Basculin", "Pom-pom Oricorio", "Pa'u Oricorio", "Sensu Oricorio"]
        seventh_set = ["Ivysaur", "Charmeleon", "Wartortle", "Raticate", "Dragonair", "Pupitar", "Shelgon", "Metang", "Gabite", "Zweilous", "Sliggoo", "Hakamo-o"]
        eight_set = ["Metapod", "Kakuna", "Pidgeotto", "Spearow", "Ekans", "Pikachu", "Sandshrew", "Nidorina", "Nidorino", "Clefairy", "Vulpix", "Jigglypuff", "Golbat", "Gloom", "Paras", "Venonat", "Diglett", "Meowth", "Psyduck", "Mankey", "Growlithe", "Poliwhirl", "Kadabra", "Machoke", "Weepinbell", "Tentacool", "Graveler", "Ponyta", "Slowpoke", "Magneton", "Doduo", "Seel", "Grimer", "Shellder", "Haunter", "Onix", "Drowzee", "Krabby", "Voltorb", "Exeggcute", "Cubone", "Lickitung", "Koffing", "Rhydon", "Chansey", "Tangela", "Seadra", "Goldeen", "Staryu", "Scyther", "Electabuzz", "Magmar", "Magikarp", "Eevee", "Omanyte", "Kabuto", "Bayleef", "Quilava", "Croconaw", "Sentret", "Hoothoot", "Ledyba", "Spinarak", "Chinchou", "Togetic", "Natu", "Flaaffy", "Marill", "Skiploom", "Aipom", "Sunkern", "Yanma", "Wooper", "Murkrow", "Misdreavus", "Pineco", "Gligar", "Snubbull", "Sneasel", "Teddiursa", "Slugma", "Piloswine", "Remoraid", "Houndour", "Phanpy", "Porygon2", "Tyrogue", "Grovyle", "Combusken", "Marshtomp", "Poochyena", "Zigzagoon", "Silcoon", "Cascoon", "Lombre", "Nuzleaf", "Taillow", "Wingull", "Kirlia", "Surskit", "Shroomish", "Vigoroth", "Nincada", "Loudred", "Makuhita", "Nosepass", "Skitty", "Lairon", "Meditite", "Electrike", "Roselia", "Gulpin", "Carvanha", "Wailmer", "Numel", "Spoink", "Vibrava", "Cacnea", "Swablu", "Barboach", "Corphish", "Baltoy", "Lileep", "Anorith", "Feebas", "Shuppet", "Dusclops", "Snorunt", "Sealeo", "Clamperl", "Grotle", "Monferno", "Prinplup", "Staravia", "Bidoof", "Kricketot", "Luxio", "Cranidos", "Shieldon", "Burmy", "Combee", "Buizel", "Cherubi", "Shellos", "Drifloon", "Buneary", "Glameow", "Stunky", "Bronzor", "Riolu", "Hippopotas", "Skorupi", "Croagunk", "Finneon", "Snover", "Servine", "Pignite", "Dewott", "Patrat", "Herdier", "Purrloin", "Pansage", "Pansear", "Panpour", "Munna", "Tranquill", "Blitzle", "Boldore", "Woobat", "Drilbur", "Gurdurr", "Palpitoad", "Swadloon", "Whirlipede", "Cottonee", "Petilil", "Krokorok", "Darumaka", "Dwebble", "Scraggy", "Yamask", "Tirtouga", "Archen", "Trubbish", "Zorua", "Minccino", "Gothorita", "Duosion", "Ducklett", "Vanillish", "Deerling", "Karrablast", "Foongus", "Frillish", "Joltik", "Ferroseed", "Klang", "Eelektrik", "Elgyem", "Lampent", "Fraxure", "Cubchoo", "Shelmet", "Mienfoo", "Golett", "Pawniard", "Rufflet", "Vullaby", "Larvesta", "Quilladin", "Braixen", "Frogadier", "Bunnelby", "Fletchinder", "Spewpa", "Litleo", "Floette", "Skiddo", "Pancham", "Espurr", "Doublade", "Spritzee", "Swirlix", "Inkay", "Binacle", "Skrelp", "Clauncher", "Helioptile", "Tyrunt", "Amaura", "Phantump", "Pumpkaboo", "Bergmite", "Noibat", "Dartrix", "Torracat", "Brionne", "Trumbeak", "Yungoos", "Charjabug", "Crabrawler", "Cutiefly", "Rockruff", "Mareanie", "Mudbray", "Dewpider", "Fomantis", "Morelull", "Salandit", "Stufful", "Steenee", "Wimpod", "Sandygast", "Thwackey", "Raboot", "Drizzile", "Skwovet", "Corvisquire", "Dottler", "Nickit", "Gossifleur", "Wooloo", "Chewtle", "Yamper", "Carkol", "Applin", "Silicobra", "Arrokuda", "Toxel", "Sizzlipede", "Clobbopus", "Sinistea", "Hattrem", "Morgrem", "Milcery", "Snom", "Cufant", "Drakloak"]
        ninth_set = ["Bulbasaur", "Charmander", "Squirtle", "Chikorita", "Cyndaquil", "Totodile", "Treecko", "Torchic", "Mudkip", "Turtwig", "Chimchar", "Piplup", "Snivy", "Tepig", "Oshawott", "Chespin", "Fennekin", "Froakie", "Rowlet", "Litten", "Popplio", "Grookey", "Scorbunny", "Sobble"]
        tenth_set = ["Rattata", "Dratini", "Larvitar", "Bagon", "Beldum", "Gible", "Deino", "Goomy", "Jangmo-o"]
        eleven_set = ["Caterpie", "Weedle", "Pidgey", "Nidoran♀️", "Nidoran♂️", "Zubat", "Oddish", "Poliwag", "Abra", "Machop", "Bellsprout", "Geodude", "Magnemite", "Gastly", "Rhyhorn", "Horsea", "Porygon", "Togepi", "Mareep", "Hoppip", "Swinub", "Wurmple", "Lotad", "Seedot", "Ralts", "Slakoth", "Whismur", "Aron", "Trapinch", "Duskull", "Spheal", "Starly", "Shinx", "Lillipup", "Pidove", "Roggenrola", "Timburr", "Tympole", "Sewaddle", "Venipede", "Sandile", "Gothita", "Solosis", "Vanillite", "Klink", "Tynamo", "Litwick", "Axew", "Fletchling", "Scatterbug", "Flabébé", "Honedge", "Pikipek", "Grubbin", "Bounsweet", "Rookidee", "Blipbug", "Rolycoly", "Hatenna", "Impidimp", "Dreepy"]
        
        if pokemon in zero_set:
            INDIVIDUAL_PERCENTAGE = "0.0007%"
            INDIVIDUAL = "142857"
                      
        elif pokemon in first_set:
            INDIVIDUAL_PERCENTAGE = "0.0011%"
            INDIVIDUAL = "90909"
                      
        elif pokemon in second_set:
            INDIVIDUAL_PERCENTAGE = "0.0022%"
            INDIVIDUAL = "45455"
                      
        elif pokemon in third_set:
            INDIVIDUAL_PERCENTAGE = "0.0045%"
            INDIVIDUAL = "22222"
                      
        elif pokemon in four_set:
            INDIVIDUAL_PERCENTAGE = "0.009%"
            INDIVIDUAL = "11111"
                      
        elif pokemon in fifth_set:
            INDIVIDUAL_PERCENTAGE = "0.024%"
            INDIVIDUAL = "4167"
                      
        elif pokemon in sixth_set:
            INDIVIDUAL_PERCENTAGE = "0.036%"
            INDIVIDUAL = "2778"
                      
        elif pokemon in seventh_set:
            INDIVIDUAL_PERCENTAGE = "0.0959%"
            INDIVIDUAL = "1043"
                      
        elif pokemon in eight_set:
            INDIVIDUAL_PERCENTAGE = "0.1439%"
            INDIVIDUAL = "695"
                      
        elif pokemon in ninth_set:
            INDIVIDUAL_PERCENTAGE = "0.1918%"
            INDIVIDUAL = "521"
                      
        elif pokemon in tenth_set:
            INDIVIDUAL_PERCENTAGE = "0.3836%"
            INDIVIDUAL = "261"
                      
        elif pokemon in eleven_set:
            INDIVIDUAL_PERCENTAGE = "0.5754%"
            INDIVIDUAL = "174"
                      
        embed=discord.Embed(title="Spawn Rate", description=f"The spawn rate for {pokemon} is {INDIVIDUAL_PERCENTAGE}\n1 {pokemon} will spawn every {INDIVIDUAL} spawns", color=0x2F3136)
        pokemon = self.bot.data.species_by_name(pokemon)

        embed.set_thumbnail(url=pokemon.image_url)
        await ctx.send(embed=embed)
        
    @checks.has_started()
    @commands.command(aliases=("wtp",))
    async def whosthatpokemon(self, ctx):
        num = random.randint(0, 890)
        
        q_url = f"https://cdn.dagpi.xyz/wtp/pokemon/{num}q.png"
        a_url = f"https://cdn.dagpi.xyz/wtp/pokemon/{num}a.png"
        
        species = self.bot.data.species_by_number(int(num))
        print(species)
        
        response = requests.get(q_url)
        file = open("whopokemon.png", "wb")
        file.write(response.content)
        file.close()
        
        embed=discord.Embed(title="Who's that pokémon?")
        
        image = discord.File("whopokemon.png", filename="poketox.png")
        embed.set_image(url="attachment://poketox.png")
        
        await ctx.send(embed=embed, file=image)
        
        response = requests.get(a_url)
        file = open("anspokemon.png", "wb")
        file.write(response.content)
        file.close()
        
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
            embed=discord.Embed(title="Times Up", description=f"The pokemon was **{species}**. You can start another one with `{ctx.prefix}whosthatpokemon`", color=0x36393F)
            image = discord.File("anspokemon.png", filename="poketox.png")
            embed.set_image(url="attachment://poketox.png")
            return await ctx.send(embed=embed, file=image)

        if message.content.lower() != species:
            embed=discord.Embed(title="Wrong", description=f"The pokemon was **{species}**. You can start another one with `{ctx.prefix}spawn easy`", color=0x36393F)
            return await message.channel.send(embed=embed)

        embed = discord.Embed(
            title=f"Correct",
            color=0x36393F
        )
        
        image = discord.File("anspokemon.png", filename="poketox.png")
        embed.set_image(url="attachment://poketox.png")
        
        return await message.reply(embed=embed, file=image,)        
        
async def setup(bot):
    print("Loaded Commands")
    await bot.add_cog(comands(bot))
