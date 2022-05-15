import discord
from discord.ext import commands
import random
import time
import math
from typing import Optional
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
from typing import Literal

class settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
      if message.author.id == 716390085896962058 and "You caught a level" in message.content:
        catch_mesg = message.content.split()
        
        #Get UserID
        res_str = catch_mesg[1].replace('!', '')
        res_str = res_str.replace('<', '')
        res_str = res_str.replace('@', '')
        catch_msg = res_str.replace('>', '')
        
        pokemon = catch_mesg[7].replace('!', '')
        
        try:
          users = self.bot.mongo.db.catchlog.find({"_id": int(catch_msg), str(ctx.guild.id): True})
            
          if users["_id"] != catch_msg:
            return
          
          try:
            start_count = int(users["count"])
            if start_count == None:
              return
            count = start_count + 1
          except:
            count = 0
            
          await message.reply(f"<@{catch_msg}> | This catch has been logged :white_check_mark:")
          
          result = await self.bot.mongo.db.catchlog.update_one(
              {"_id": catch_msg},
              {"$unset": {"count": str(count)}},
              {"$unset": {"recent_catch": str(pokemon)}},
              upsert=True,
          )
          
        except:
            return
        
async def setup(bot):
    print("Loaded Settings")
    await bot.add_cog(settings(bot))
