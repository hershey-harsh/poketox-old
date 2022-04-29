import os
import discord
from discord.ext import commands, events
from discord.ext.events import member_kick
import datetime
import config

COGS = [
    "data",
    "mongo",
    "pokedex",
    "collectors",
    "shinyhunt",
    "identify",
    "info",
    "weakness",
    "dex",
    "bot",
    "raredex",
    "help",
    "comands",
    "admin",
    "rep",
    "feedback",
    "economy"
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
      
        self.config = config
        os.system("clear")
        self.remove_command("help")
        
        async def setup_hook(self):
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

if __name__ == "__main__":
    bot = Bot()
    bot.run(config.BOT_TOKEN)
