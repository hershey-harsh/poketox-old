from typing import Dict
from discord.ext import commands, ipc
from discord.ext.ipc.server import Server
from discord.ext.ipc.errors import IPCError
from discord.ext.ipc.objects import ClientPayload

class Routes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        if not hasattr(bot, "ipc"):
            bot.ipc = ipc.Server(self.bot, host="127.0.0.1", standard_port=1025, secret_key="OTI5MjIxNDQwMzA0MjA5OTkw")
    
    async def cog_load(self) -> None:
        await self.bot.ipc.start()

    async def cog_unload(self) -> None:
        await self.bot.ipc.stop()
        self.bot.ipc = None

    @Server.route()
    async def get_user_data(self, data: ClientPayload) -> Dict:
        user = await self.bot.fetch_user(data.user_id)
        return user._to_minimal_user_json()

async def setup(bot):
    await bot.add_cog(Routes(bot))
