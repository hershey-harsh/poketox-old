import sys
import logging
import discord

from discord.ext import commands, ipc
from discord.ext.ipc.server import route
from discord.ext.ipc.errors import IPCError

class Routes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        if not hasattr(bot, "ipc"):
            bot.ipc = ipc.Server(self.bot, host="127.0.0.1", port=2300, secret_key="2022poketox2007")
            bot.ipc.start()
        for name, function in inspect.getmembers(self):
            if name.startswith("get_"): # ATTENTION: Every function that stats with `get_` will be registered as endpoint
                bot.ipc.endpoints[name] = function
    
    @commands.Cog.listener()
    async def on_ipc_ready(self):
        logging.info("Ipc is ready")
    
    @commands.Cog.listener()
    async def on_ipc_error(self, endpoint: str, error: IPCError):
        logging.error(endpoint, "raised", error, file=sys.stderr)

    async def get_user_data(self, data):
        user = self.bot.get_user(data.user_id)
        return user._to_minimal_user_json() # THE OUTPUT MUST BE JSON SERIALIZABLE!

async def setup(bot):
    await bot.add_cog(Routes(bot))
