import subprocess
import os

#Installs all the dependencies automatically.
#The only problem is people usually have multiple virtual environments and their pip version might be different.

def install(name):
  subprocess.call(['pip', 'install', name])
install("git+https://github.com/iDevision/enhanced-discord.py@edpy-legacy")

os.system("clear")

import discord
from discord.ext import commands, events
from discord.ext.events import member_kick
import datetime
import config
import keep_alive

COGS = [
    "data",
    "mongo",
    "pokedex",
    "collectors",
    "shinyhunt",
    "identify",
    "info",
    "weakness",
    "dex"
]


class Bot(commands.Bot, events.EventsMixin):
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            command_prefix=[config.PREFIX, "A!"], self_bot=False, slash_commands=True, intents=discord.Intents.all(),
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, replied_user=False),
            case_insensitive=True,
        )
      
        self.config = config



        for i in COGS:
            self.load_extension(f"cogs.{i}")
        
    @property
    def mongo(self):
        return self.get_cog("Mongo")

    @property
    def data(self):
        return self.get_cog("Data").instance

    async def on_ready(self):
        self.log.info(f"Logged in")

if __name__ == "__main__":
    bot = Bot()
    bot.remove_command('help')
    keep_alive.keep_alive()
    bot.run(config.BOT_TOKEN)
