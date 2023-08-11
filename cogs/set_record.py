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

class Set_record(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def module(self,ctx,content:str):
        client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
        db = client['rlog']
        collection = db[f'{ctx.guild.id}']
        # Only respond to commands from users with the correct permissions
        if not ctx.author.guild_permissions.administrator:
            await ctx.channel.send('권한이 없습니다', delete_after=1)
            return

        # Use the current channel if no channel is specified
        

        # Insert a new document in the collection
        try:
            db[str(ctx.guild.id)].insert_one({'channel_id': f'{ctx.channel.id}', 'content': content})
        except pymongo.errors.PyMongoError:
            await ctx.channel.send('데이터베이스 오류', delete_after=1)
            return

        await ctx.channel.send(f'{content} 내용이 {ctx.channel.name} 에 기록됨!\n기록이 잘린다면 슬래시 커맨드로 사용해 주세요', delete_after=2)
    
    # @commands.command(name='기록')
    # async def prefix(self,ctx: commands.Context,*args):
    #     a=args[0:]
    #     content=' '.join(s for s in a)
    #     await self.module(ctx,content)
                
    @commands.hybrid_command ( name = '기록', with_app_command = True,description="채널에 셋팅내용을 기록합니다." )
    @commands.guild_only()
    async def slash_with_app_command(self, ctx: commands.Context,*,content:str):
            if hasattr(ctx, 'interaction') and ctx.interaction is not None:
                await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
            await self.module(ctx,content)
            
async def setup(bot):
    await bot.add_cog(Set_record(bot), guilds=None)  # Add guild IDs if needed