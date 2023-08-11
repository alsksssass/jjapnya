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

class Nick_reset(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def del_nick(self,ctx):
        if ctx.author.guild_permissions.administrator:

            guild_id = str(ctx.guild.id)
            client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
            db = client['nickdatabase']
            collection = db[guild_id]

            # Get the guild ID
            guild_id = str(ctx.guild.id)

            # Get the collection for the guild
            collection = db[guild_id]

            # Extract the channel ID from the command
            channel_id = str(ctx.channel.id)

            # Delete the document with the matching channel ID
            result = collection.delete_many({})

            if result.deleted_count > 0:
                await ctx.send(f'모든 닉네임이 삭제되었습니다!', delete_after=2.0)
            else:
                await ctx.send(f'이미 모두 초기화 되었습니다.', delete_after=2.0)
        else:
                await ctx.channel.send('권한이 없습니다', delete_after=1)
    
    # @commands.command(name='닉초기화')
    # async def prx(self,ctx: commands.Context):
    #     await self.del_nick(ctx)
                
    @commands.hybrid_command ( name = '닉초기화', with_app_command = True,description="!캐릭터 명령어 오류시 사용!" )
    @commands.guild_only()
    async def slash_with_app_command(self, ctx: commands.Context):
            if hasattr(ctx, 'interaction') and ctx.interaction is not None:
                await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
            await self.del_nick(ctx)
            
async def setup(bot):
    await bot.add_cog(Nick_reset(bot), guilds=None)  # Add guild IDs if needed