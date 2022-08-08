import sys
import logging
import discord
import inspect

from discord.ext import commands, ipc
from discord.ext.ipc.server import route
from discord.ext.ipc.errors import IPCError
from flask import Flask

from aiohttp import web
from discord.ext import commands, tasks
import discord
import os
import aiohttp

app = web.Application()

class Routes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.web_server.start()
    
    @routes.get('/test')
    def home():
        return "I'm alive"
    
    @tasks.loop()
    async def web_server(self):
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host='134.209.35.31', port=5000)
        await site.start()
        
    @web_server.before_loop
    async def web_server_before_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Routes(bot))
