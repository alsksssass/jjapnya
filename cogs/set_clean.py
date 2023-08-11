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

class Set_clean(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def module(self,ctx):
        client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
        db = client['rlog']
        collection = db[str(ctx.guild.id)]
        # Only respond to commands from users with the correct permissions
        if not ctx.author.guild_permissions.administrator:
                await ctx.send('권한이 없습니다', delete_after=1)
                return
        # Extract the channel ID from the command
        channel_id = str(ctx.channel.id)
        print(channel_id)

        # Delete all documents with the channel ID in the collection
        result = collection.delete_many({"channel_id": channel_id})
        
        await ctx.channel.send(f'{ctx.channel.name}에 기록된 데이터 {result.deleted_count}개 삭제됨 ')
    
    # @commands.command(name='기록삭제')
    # async def prefix(self,ctx: commands.Context):
    #     await self.module(ctx)
                
    @commands.hybrid_command ( name = '기록삭제', with_app_command = True,description="현재 채널에 기록된 셋팅내용을 삭제합니다." )
    @commands.guild_only()
    async def slash_with_app_command(self, ctx: commands.Context):
            if hasattr(ctx, 'interaction') and ctx.interaction is not None:
                await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
            await self.module(ctx)
            
async def setup(bot):
    await bot.add_cog(Set_clean(bot), guilds=None)  # Add guild IDs if needed