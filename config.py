import os
import random
import discord

def RATES(bet):
  number = random.randint(0, 11)
  if number > 6: # the random function of the gambling games
    return True

BOT_TOKEN = os.getenv("Discord_Token")
DATABASE_URI = "mongodb+srv://xen:discord@cluster0.ygld5.mongodb.net/discord?retryWrites=true&w=majority"
DATABASE_NAME = "discord"
DEFAULT_PREFIX = "a!"
PREFIX = "a!"

ERROR_COLOR= discord.Color.red()

SERVER_FILE_LOCATION = "data/servers.json"
STATS_FILE_LOCATION = "data/stats.json"
FAV_FILE_LOCATION = "data/fav.json"
TAG_FILE_LOCATION = "data/tags.json"
MOVESET_FILE_LOCATION = "data/moveset.json"
BATTLE_LOG_FILE_LOCATION = "data/battle_log.json"
ALT_NAME_FILE_LOCATION = "data/poke_alt_names.json"
RARITY_FILE_LOCATION = "data/poke_rarity.json"
NATURE_FILE_LOCATION = "data/nature.json"
TYPE_FILE_LOCATION = "data/type_data.json"
WEAKNESS_FILE_LOCATION = "data/weakness_data.json"

TIER_LINK = {
    "rare" : "https://media.discordapp.net/attachments/793689115689353247/924912850953195520/IMG_0018.png",
    "mega" : "https://cdn.discordapp.com/attachments/774499540938129429/870761603153416202/my-image_50.png",
    "bug" : "https://media.discordapp.net/attachments/774499540938129429/845692957214375966/image0.png",
    "dark" : "https://cdn.discordapp.com/attachments/918973688932630589/935020376717672448/my-image_6.png",
    "dragon" : "https://cdn.discordapp.com/attachments/793689115689353247/931947498937921596/my-image_3.png",
    "electric" : "https://cdn.discordapp.com/attachments/793689115689353247/868569489938210836/my-image_46.png",
    "fairy" : "https://cdn.discordapp.com/attachments/793689115689353247/936020121900703744/my-image_11.png",
    "fighting" : "https://cdn.discordapp.com/attachments/718008298837770290/901298772783558716/my-image_14.png",
    "fire" : "https://cdn.discordapp.com/attachments/899753866638266418/900555487437807657/my-image_11.png",
    "flying" : "https://cdn.discordapp.com/attachments/774499540938129429/887928654116552724/my-image.png", 
    "ghost" : "https://media.discordapp.net/attachments/718008298837770290/844752635684454460/image0.png",
    "grass" : "https://media.discordapp.net/attachments/793689115689353247/920423300692332564/IMG_9676.png",
    "ground" : "https://cdn.discordapp.com/attachments/718008298837770290/866929735920254976/my-image_43.png",
    "ice" : "https://media.discordapp.net/attachments/774499540938129429/850456657120591943/my-image_9.png",
    "normal" : "https://cdn.discordapp.com/attachments/718008298837770290/896314513895329853/my-image_1.png",
    "poison" : "https://cdn.discordapp.com/attachments/718008298837770290/934966138415239198/my-image_4.png",
    "psychic" : "https://cdn.discordapp.com/attachments/877212831240560752/909264788935311360/my-image_17.png",
    "rock" : "https://cdn.discordapp.com/attachments/718008298837770290/900550270050787358/my-image_8.png",
    "steel" : "https://cdn.discordapp.com/attachments/918973688932630589/935029992541278208/my-image_8.png",
    "water" : "https://cdn.discordapp.com/attachments/774499540938129429/876979764773126225/my-image_55.png"
}

#772937584884056135 | Dank City | Premium Lifetime
#848582111577505802 | Pichus Playground | Unlimited | May 13th
#844392814485831710, 856328341702836265, 772557819303297054, 849169202966429696 | AndoCommanndo#3321 | May 17th
#815598238820335668 | Future World | Unlimited | Forever
#843415018090528778 | Pokefever | Unlimited | 10k Members Forver

basic_premium=[]
premium=[772937584884056135]
unlimited_premium=[848582111577505802, 844392814485831710, 856328341702836265, 772557819303297054, 849169202966429696, 815598238820335668, 843415018090528778]
