import os
import discord
from discord.ext import commands, events
from discord.ext.events import member_kick
import datetime
import helpers
from helpers import checks
from helpers import context
import aiohttp
import config

COGS = [
    "data",
    "mongo",
    "settings",
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
]

intents = discord.Intents.default()
intents.message_content = True

class Bot(commands.Bot, events.EventsMixin):
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            command_prefix=[config.PREFIX, "A!"], self_bot=False, owner_id = [790788488983085056, 679159125762113537], slash_commands=True, intents=intents,
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=True, replied_user=False),
            case_insensitive=True,
        )
      
        self.config = config
        os.system("clear")
        self.remove_command("help")
        
    async def setup_hook(self):
        self.http_session = aiohttp.ClientSession()
        await self.load_extension("jishaku")
        for i in COGS:
            await self.load_extension(f"cogs.{i}")
            
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
    
    async def get_context(self, message, *, cls=context.PoketwoContext):
        return await super().get_context(message, cls=cls)

if __name__ == "__main__":
    bot = Bot()
    os.system('clear')
    bot.run(config.BOT_TOKEN)
