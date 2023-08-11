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

class N_list(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def show_list(self,ctx):
        try:
            if ctx.author.guild_permissions.administrator:
                guild_id = str(ctx.guild.id)
                client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
                db = client['nickdatabase']
                collection = db[guild_id]

                # Get the guild ID
                guild_id = str(ctx.guild.id)

                # Get the collection for the guild
                collection = db[guild_id]

                # Find all documents in the collection with the guild ID

                nick_names=[]
# Iterate over the documents and extract nick_name and roll values

                documents = collection.find({})

# Iterate over the documents and extract nick_name and roll values
                for document in documents:
                    nick_name = document['nick_name']
                    roll = document.get('roll', '없음')  # Get the 'roll' value, default to '없음' if it doesn't exist
                    if not roll:
                        roll = '없음'
                    # Create and send the message
                    nick_names.append(f"닉네임: {nick_name}\n역할: {roll}\n")
                    # await ctx.send(message)
                
                    
                

                    
                # Create a list of channel objects using the channel IDs



                
                result = ''.join(s for s in nick_names)

                channel_count=len(nick_names)
                
                # Display the list of channels
                await ctx.reply(f'캐릭터 닉네임 {channel_count} 개 :\n{result}')
                

            else:
                await ctx.channel.send('권한이 없습니다', delete_after=1)
        except Exception as e:
            print(e)
            await ctx.send('오류발생시 ``!닉초기화`` 명령어 사용후 다시 추가해 주세요!')
        

    # @commands.command(name='닉보기')
    # async def prx_add(self, ctx: commands.Context):
    #     await self.show_list(ctx)

    @commands.hybrid_command ( name = '닉보기', with_app_command = True,description="!캐릭터 에 나오는 닉 리스트를 보여줍니다." )
    @commands.guild_only()
    async def add_with_app_command(self, ctx: commands.Context):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.show_list(ctx)

async def setup(bot):
    await bot.add_cog(N_list(bot), guilds=None) 
