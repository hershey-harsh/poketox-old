import os
import discord
from discord.ext import commands, events, ipc
from discord.ext.events import member_kick
import datetime
import helpers
from helpers import checks
from helpers import context
import aiohttp
from termcolor import colored, cprint
import config

COGS = [
    "data",
    "mongo",
    "settings",
    "collectors",
    "comands",
    "region",
    "shinyhunt",
    "pokedex",
    "identify",
    "ipc"
    "spawn_counts",
    "info",
    "weakness",
    "dex",
    "bot",
    "raredex",
    "help",
    "admin",
    "feedback",
    "economy",
    "predict_app",
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
        
        self.ipc = ipc.Server(self, secret_key="192b9bdd21ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d53727823bcbf")
      
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
        
    os.system("clear")
    
    async def on_ipc_ready(self):
        """Called upon the IPC Server being ready"""
        cprint("IPC Server is online.", 'green')
        
    async def on_ipc_error(self, endpoint, error):
        """Called upon an error being raised within an IPC route"""
        print(endpoint, "raised", error)
        
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
    bot.ipc.start()
    bot.run(config.BOT_TOKEN)
