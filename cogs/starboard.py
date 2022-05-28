legendaries = ["Nihilego", "Buzzwhole", "Pheromosa", "Xurkitree", "Celesteela", "Kartana", "Guzzlord", "Poipole", "Naganadel", "Stakataka", "Blacephallon", 'Articuno', 'Zapdos', 'Moltres', 'Mewtwo', 'Raikou', 'Entei', 'Suicune', 'Lugia', 'Ho-Oh ', 'Regirock', 'Regice', 'Registeel ', 'Latias', 'Latios ', 'Kyogre ', 'Groudon', 'Rayquaza', 'Uxie', 'Azelf', 'Mesprit', 'Dialga ', 'Palkia', 'Heatran', 'Regigigas', 'Giratina', 'Cresselia', 'Cobalion', 'Terrakion', 'Virizion', 'Tornados', 'Thundurus', 'Reshiram', 'Zekrom ', 'Landorus', 'Kyurem', 'Xerneas', 'Yveltal', 'Zygarde', 'Type:Null', 'Silvally', 'Tapu Koko', 'Tapu Lele', 'Tap Bulu', 'Tapu Fini', 'Cosmog ', 'Cosmoem', 'Solgaleo', 'Lunala', 'Necrozma ', 'Zacian', 'Zamazenta ', 'Eternatus ', 'Kubfu ', 'Urshifu ', 'Regieleki', 'Regidrago', 'Glastrier ', 'Spectrier', 'Calyrex', 'Galarian Articuno', 'Galarian Moltres', 'Galarian Zapdos', 'Mew ', 'Celebi', 'Jirachi ', 'Deoxys ', 'Phione', 'Manaphy', 'Darkrai', 'Shaymin', 'Arceus ', 'Victini', 'Keldeo', 'Meloetta', 'Genesect', 'Diancie', 'Hoopa ', 'Volcanion', 'Magearna', 'Marshadow ', 'Zeraora', 'Meltan', 'Melmetal', 'Zarude', 'Galarian Zigzagoon', 'Galarian Linoone', 'Obstagoon', 'Galarian Meowth', 'Perrserker', 'Galarian Ponyta', 'Galarian Rapidash', 'Galarian Slowpoke', 'Galarian Slowbro', 'Galarian Slowking', 'Galarian Corsola', 'Cursola', 'Galarian Farfetch’d', "Sirfetch'd", 'Galarian Weezing', 'Galarian Mr. Mime', 'Mr. Rime', 'Galarian Darumaka', 'Galarian Darmanitan', 'Galarian Yamask', 'Runerigus', 'Galarian Stunfisk', 'Alolan Rattata', 'Alolan Raticate', 'Alolan Raichu', 'Alolan Sandshrew', 'Alolan Sandslash', 'Alolan Vulpix', 'Alolan Ninetales', 'Alolan Diglett', 'Alolan Dugtrio', 'Alolan Meowth', 'Alolan Persian', 'Alolan Geodude', 'Alolan Graveler', 'Alolan Golem', 'Alolan Grimer', 'Alolan Muk', 'Alolan Exeggutor', 'Alolan Marowak']

class starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
      def check(m):
        return m.channel == message.channel and m.author != client.user and "You caught a" in m.content
      if message.author.id == 716390085896962058 and message.guild.id ==803413582988967976:
        if message.embeds:
          title = message.embeds[0].title
       
          if "wild" in title:

            while True:
              response = await client.wait_for('message', check = check, timeout=300) 
              if "You caught a" in response.content:
                break
            name = response.content.split(" ")[7]
            name = name.replace("!","")
            
            if name in legendaries:
              
              embed=discord.Embed(title=title, description="Guess the pokémon and type `.catch <pokémon>` to catch it!", color=0x36393F)
              embed.set_author(name="Pokétwo", icon_url="https://images-ext-2.discordapp.net/external/o_exZBgx6nWOaTdvEuMkhmZ-ig_Yr0igDiy5MQ8Zs1o/https/cdn.discordapp.com/avatars/716390085896962058/2489a9b2c2eb951ed908be416ced10a2.png")
              embed.add_field(name="Jump to message", value=f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}")
              embed.set_image(url = message.embeds[0].image.url)
              
              ctx = await self.bot.get_context(message)
              guild = await ctx.bot.mongo.fetch_guild(ctx.guild)
              
              channelid = int(guild["starboard"])
              await client.get_channel(channelid).send(embed=embed)
        
async def setup(bot):
    print("Loaded Starboard")
    await bot.add_cog(starboard(bot))
