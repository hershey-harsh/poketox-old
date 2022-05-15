import os
import discord
from discord.ext import commands, events
from discord.ext.events import member_kick
import datetime
import config

print("Loaded Check #1")

COGS = [
    "data",
    "mongo",
    "settings",
    "pokedex",
    "collectors",
    "shinyhunt",
    "identify",
    "spawn_counts",
    "info",
    "weakness",
    "dex",
    "bot",
    "raredex",
    "help",
    "comands",
    "admin",
    "feedback",
    "economy",
    "catch_tracker"
]

intents = discord.Intents.default()
intents.message_content = True

class Bot(commands.Bot, events.EventsMixin):
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            command_prefix=[config.PREFIX, "A!"], self_bot=False, owner_id = 790788488983085056, slash_commands=True, intents=intents,
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=True, replied_user=False),
            case_insensitive=True,
        )
        
        print("Loaded Check #2")
      
        self.config = config
        os.system("clear")
        self.remove_command("help")
        
        print("Loaded Check #3")
        
    async def on_ready(self):
        print("Bot ready!")
            
        print("Loaded Check #4")
        
    async def setup_hook(self):
        await self.load_extension("jishaku")
        for i in COGS:
            print("Loading")
            await self.load_extension(f"cogs.{i}")
            
        print("Loaded Check #5")
            
        self.add_check(
            commands.bot_has_permissions(
                read_messages=True,
                send_messages=True,
                embed_links=True,
                read_message_history=True,
                add_reactions=True,
                external_emojis=True,
            ).predicate
        )

        
    @property
    def mongo(self):
        return self.get_cog("Mongo")

    @property
    def data(self):
        return self.get_cog("Data").instance

if __name__ == "__main__":
    bot = Bot()
    bot.run(config.BOT_TOKEN)
