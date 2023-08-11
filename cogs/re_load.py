import discord
from discord import ui
from discord.ui import Button, View
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure, HybridCommand
import time
import os
import pymongo
from datetime import datetime
import asyncio
from asyncio import sleep
import json 
import socket
import discord.utils
import requests
from pydub import AudioSegment
import urllib.request
import re
from urllib.parse import urlparse
from discord import Embed
import openpyxl

class Re_load(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def 리로드(self, ctx, extension):
        if ctx.author.id == 317655426868969482:
            try:
                cog_name = f'cogs.{extension}'
                if cog_name in self.bot.extensions:
                    # Unload the extension
                    await self.bot.unload_extension(cog_name)

                # Load the extension
                await self.bot.load_extension(cog_name)
                
                if hasattr(self.bot, "sync_commands"):
                    await self.bot.sync_commands()

                await ctx.send(f'{extension} Cog을(를) 리로드했습니다.')
            except Exception as e:
                await ctx.send(f'오류: {type(e).__name__} - {e}')
        else:
            return

async def setup(bot):
    await bot.add_cog(Re_load(bot), guilds=None) 