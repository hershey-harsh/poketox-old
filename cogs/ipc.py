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

    @Server.route()
    async def get_all_channels(self, data: ClientPayload) -> Dict:
        guild_id = data.guild_id
        
        text_channel_names = []
        guild = self.bot.get_guild(int(guild_id))
        for channel in guild.text_channels:
            text_channel_names.append(f'#{channel.name}')
   
    @Server.route()
    async def get_mutual_guilds(self, data: ClientPayload) -> Dict:
        guild_ids = data.guild_ids
        
        if not guild_ids:
            return {"error": "Invalid guilds"}

        guilds = []
        for i in guild_ids:
            guild: discord.Guild = self.bot.get_guild(int(i))
            if not guild:
                continue
            if guild.get_member(self.bot.user.id):
                
                if guild.icon is not None:
                    icon=str(guild.icon.url)
                    
                else:
                    icon = None
                    
                guilds.append({
                    "id": str(guild.id),
                    "name": guild.name,
                    "icon_url": icon
                })
                
        return {"guilds": guilds}
    
    stuff = """
    @Server.route()
    async def clear_user_list(self, data: ClientPayload) -> Dict:
        list = data.list
        try:
            if list == "collectlist":
                await self.bot.mongo.db.collector.delete_one({"_id": int(data.user_id)})
            if list == "shinyhunt":
                await self.bot.mongo.db.shinyhunt.update_one({"_id": int(data.user_id)}, {"$set": {'shinyhunt': None}}, upsert=True)
            if list == "regionhunt":
                await self.bot.mongo.db.regionlist.delete_one({"_id": ctx.author.id})
            if list == "regionform":
                await self.bot.mongo.db.regionformlist.delete_one({"_id": ctx.author.id})
            return {"code":"200"}
        except Exception as e:
            return {"code":"400", "error":str(e)}

    @Server.route()
    async def clear_user_list(self, data: ClientPayload) -> Dict:
    """
        
async def setup(bot):
    await bot.add_cog(Routes(bot))
