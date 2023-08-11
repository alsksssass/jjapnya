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

class De_channel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def De_channel_log(self,ctx):
        if ctx.author.guild_permissions.administrator:
            client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
            db = client['mydatabase']

            # Get the guild ID
            guild_id = str(ctx.guild.id)

            # Get the collection for the guild
            collection = db[guild_id]

            # Extract the channel ID from the command
            channel_id = str(ctx.channel.id)

            # Delete the document with the matching channel ID
            result = collection.delete_one({'channel_id': channel_id})

            if result.deleted_count > 0:
                await ctx.channel.send(f'{ctx.channel.name}이(가) 삭제되었습니다!', delete_after=2)
            else:
                await ctx.channel.send(f'{ctx.channel.name}은 삭제 리스트에 존재하지 않습니다', delete_after=2)

        else:
                await ctx.channel.send('권한이 없습니다', delete_after=1)
        
        

    # @commands.command(name='제외')
    # async def prx_add(self, ctx: commands.Context):
    #     await self.De_channel_log(ctx)

    @commands.hybrid_command ( name = '제외', with_app_command = True,description="삭제 채널리스트에서 현재 채널을 제외합니다." )
    @commands.guild_only()
    async def add_with_app_command(self, ctx: commands.Context):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.De_channel_log(ctx)

async def setup(bot):
    await bot.add_cog(De_channel(bot), guilds=None) 