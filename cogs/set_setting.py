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

class Set_setting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def module(self,ctx):
    # Only respond to commands from users with the correct permissions
        if not ctx.author.guild_permissions.administrator:
            await ctx.send('권한이 없습니다', delete_after=1)
            return
        # Get the guild ID
        guild_id = str(ctx.guild.id)

        # Connect to the MongoDB database
        client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
        db = client['rlog']
        collection = db[str(guild_id)]

        # Get all the documents in the collection
        results = collection.find()

        # Loop through the documents and send the content to the channel
        for result in results:
            channel_id = result['channel_id']
            content = result['content']
            if content is None:
                content='없음'
            try:
                channel = await self.bot.fetch_channel(int(channel_id))
                await channel.send(content)
            except discord.errors.NotFound:
                pass

        await ctx.send('셋팅 완료!', delete_after=1)
        
        

    # @commands.command(name='셋팅')
    # async def prx_add(self, ctx: commands.Context):
    #     await self.module(ctx)

    @commands.hybrid_command ( name = '셋팅', with_app_command = True,description="기록으로 기록된 채널의 내용들을 모두 불러옵니다." )
    @commands.guild_only()
    async def add_with_app_command(self, ctx: commands.Context):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.module(ctx)

async def setup(bot):
    await bot.add_cog(Set_setting(bot), guilds=None) 