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
import yt_dlp
from discord import FFmpegPCMAudio
import isodate

def get_video_info(url):
    YOUTUBE_API_KEY ='AIzaSyDfcoQyQq2lcevMuF0_6sngn-8ww5d1M68'
    video_id=url.replace('https://www.youtube.com/watch?v=', '')

    video_info_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={video_id}&key={YOUTUBE_API_KEY}"
    video_info_response = requests.get(video_info_url)
    video_info = video_info_response.json()["items"][0]
    content_details = video_info["contentDetails"]
    snippet = video_info["snippet"]
    video_duration = content_details["duration"]
    video_duration_seconds = int(isodate.parse_duration(video_duration).total_seconds())
    video_title = snippet['title']

    return {
        # 'url': f"https://www.youtube.com/watch?v={video_id}",
        'title': video_title,
        'duration': video_duration_seconds,
        'thumbnail': f"https://img.youtube.com/vi/{video_id}/0.jpg"
    }

class U_name_add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    async def add_u_link(self,ctx,m_name:str,url:str):
        # Only respond to commands from users with the correct permissions
        if ctx.author.guild_permissions.administrator:
            guild_id = str(ctx.guild.id)
            client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
            db = client['music']
            collection = db[guild_id]
            video_info = get_video_info(url)
            info=video_info['title']
            # db = client['mydatabase']
            # collection = db['channels']

            # Check if the channel ID is already in the collection
            existing_channel = collection.find_one({'name': m_name})
            if existing_channel:
                await ctx.channel.send(f'{m_name}은 이미 추가된 이름입니다', delete_after=2)
            elif video_info is None:
                await ctx.channel.send(f'주소가 정확하지 않습니다.', delete_after=2)
            else:

                # Insert a new document in the collection
                collection.insert_one({'name': m_name, 'url': url, 'info': info})
                await ctx.channel.send(f'{m_name}이(가) 유튜브 목록에 이름 추가됨!', delete_after=2)
        else:
            await ctx.channel.send('권한이 없습니다', delete_after=1)
    async def DEL_U_name(self,ctx,m_name:str):
        guild_id = str(ctx.guild.id)
        client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
        db = client['music']
        collection = db[guild_id]
        result = collection.delete_one({'name': m_name})

        if result.deleted_count > 0:
            await ctx.channel.send(f'{m_name}이(가) 삭제되었습니다!', delete_after=2)
        else:
            await ctx.channel.send(f'{m_name}은 리스트에 존재하지 않습니다', delete_after=2)
    
    
    # @commands.command(name='저장')
    # async def prx1(self,ctx: commands.Context,m_name:str,url:str):
    #     await self.add_u_link(ctx,m_name,url)
                
    @commands.hybrid_command ( name = '저장', with_app_command = True,description="!유트브 링크를 이름으로 저장합니다." )
    @commands.guild_only()
    async def slash_with_app_command1(self, ctx: commands.Context,이름:str,url:str):
            
            m_name=이름
            if hasattr(ctx, 'interaction') and ctx.interaction is not None:
                await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
            await self.add_u_link(ctx,m_name,url)
    
    # @commands.command(name='저장삭제')
    # async def prx(self,ctx: commands.Context,m_name:str):
    #     await self.DEL_U_name(ctx,m_name)
                
    @commands.hybrid_command ( name = '저장삭제', with_app_command = True,description="저장된 유튜브링크 삭제" )
    @commands.guild_only()
    async def slash_with_app_command(self, ctx: commands.Context,*,이름:str):
            
            m_name=이름
            if hasattr(ctx, 'interaction') and ctx.interaction is not None:
                await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
            await self.DEL_U_name(ctx,m_name)
            
async def setup(bot):
    await bot.add_cog(U_name_add(bot), guilds=None)  # Add guild IDs if needed