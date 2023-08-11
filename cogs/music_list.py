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

class M_list(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def show_list(self,ctx):
        if ctx.author.guild_permissions.administrator:

            # Check if the './sound/' directory exists
            if not os.path.isdir('./sound/'):
                await ctx.channel.send("리스트가 없습니다.")
                
            
            if not os.path.isdir(f'./sound/{ctx.guild.id}/'):
                await ctx.channel.send(f"{ctx.guild.name} 에 등록된 개인 음악 리스트가 없습니다.")
                

            if  os.path.isdir(f'./sound/{ctx.guild.id}/'):
                p_file_list = [f for f in os.listdir(f'./sound/{ctx.guild.id}/')]
                message2 = f"{ctx.guild.name} 의 개인 음성파일 리스트입니다.:\n"
                for file in p_file_list:
                    message2 += f"- {file}\n"
                await ctx.author.send(content=message2)
                await ctx.channel.send('개인파일 리스트는 DM으로 전송되었습니다.')
            
            # Get a list of MP3 files in the './sound/' directory
            file_list = [f for f in os.listdir('./sound/') if os.path.isfile(os.path.join('./sound/', f))]


            # Check if the './sound/{ctx.author.id}/' directory exists


            # Format the list of filenames into a message
            message = "음성파일 리스트입니다.:\n"
            for file in file_list:
                message += f"- {file}\n"
            
            await ctx.channel.send(message)

            
            guild_id = str(ctx.guild.id)
            client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
            db = client['music']
            collection = db[guild_id]
            songs = collection.find({}, {'url': 0})  # 수정된 부분입니다.
            print(songs)
            if collection.count_documents({}) > 0:
                message4 = "유튜브저장 리스트입니다:\n"
                for song in songs:
                    print(song)
                    name = song['name']
                    if 'info' in song :
                        info = song['info']
                        message4 += f"- 이름:{name} ℹ️정보:{info}\n"
                    else:
                        message4 += f"- 타이틀:{name} \n"
                
                await ctx.send(message4)
                
            else:
                await ctx.send('유튜브저장 음악이 없습니다.')

        else:
                await ctx.channel.send('권한이 없습니다', delete_after=1)
        
        

    # @commands.command(name='음악목록')
    # async def prx_add(self, ctx: commands.Context):
    #     await self.show_list(ctx)

    @commands.hybrid_command ( name = '음악목록', with_app_command = True,description="플레이 가능한 음악 목록을 보여줍니다." )
    @commands.guild_only()
    async def add_with_app_command(self, ctx: commands.Context):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.show_list(ctx)

async def setup(bot):
    await bot.add_cog(M_list(bot), guilds=None) 