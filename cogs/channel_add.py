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

class add_channel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def Add_channel_del(self,ctx):
        # Only respond to commands from users with the correct permissions
        if ctx.author.guild_permissions.administrator:
            # Extract the channel ID from the command
            channel_id = str(ctx.channel.id)
            # Get the guild ID
            guild_id = str(ctx.guild.id)
            client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
            db = client['mydatabase']
            collection = db[guild_id]

            # db = client['mydatabase']
            # collection = db['channels']

            # Check if the channel ID is already in the collectionㄷ
            existing_channel = collection.find_one({'channel_id': channel_id})
            if existing_channel:
                channel = self.bot.get_channel(int(channel_id))
                await ctx.channel.send(f'{channel.name}은 이미 추가된 채널입니다', delete_after=2)
            else:
                # Get the channel object using its ID
                channel = self.bot.get_channel(int(channel_id))
                # Insert a new document in the collection
                collection.insert_one({'channel_id': channel_id, 'channel_name': channel.name})
                await ctx.channel.send(f'{channel.name}이(가) 삭제 리스트에 추가됨!', delete_after=2)

        
        else:
            await ctx.channel.send('권한이 없습니다', delete_after=1)
        
        

    # @commands.command(name='추가')
    # async def prx_add(self, ctx: commands.Context):
    #     await self.Add_channel_del(ctx)

    @commands.hybrid_command ( name = '추가', with_app_command = True,description="고양이 명령어로 한번에 삭제할 채널을 추가합니다." )
    @commands.guild_only()
    async def add_with_app_command(self, ctx: commands.Context):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.Add_channel_del(ctx)

async def setup(bot):
    await bot.add_cog(add_channel(bot), guilds=None) 