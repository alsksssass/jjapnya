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
from discord import Thread

class Cat_del(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def delete_messages(channel):
        while True:
            messages = []
            async for message in channel.history(limit=99):
                if not isinstance(message, discord.MessageType.default):
                    messages.append(message)
            
            if not messages:
                break
            else:
                non_system_messages = [msg for msg in messages if msg.type == discord.MessageType.default]
                if not non_system_messages:
                    break
                    
                try:
                    await channel.delete_messages(non_system_messages)
                except discord.exceptions.Forbidden as e:
                    print(f"에러: {str(e)}, 메시지 삭제 실패")
                    break
            
    async def cat_channel_del(self,ctx):
        try:
            if ctx.author.guild_permissions.administrator:
                guild_id = str(ctx.guild.id)
                client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
                db = client['mydatabase']
                collection = db[guild_id]
                # Get the guild ID
                # Read the list of channel IDs and names from the file
                # with open(f'{guild_id}_channels.txt', 'r') as f:
                documents = collection.find()
                
                # Create a list of channel IDs and names from the documents
                channels_to_delete = []
                for doc in documents:
                    try:
                        channel_id = doc['channel_id']
                        channel_name = doc['channel_name']
                        channels_to_delete.append(f"{channel_id},{channel_name}")
                        channel = self.bot.get_channel(int(channel_id))
                        
                        while True:
                            messages = []
                            async for message in channel.history(limit=99):
                                messages.append(message)
                                # await channel.delete_messages(messages)
                            if not messages:
                                break
                            
                            await channel.purge(bulk=True)
                        await channel.send(f'{channel.name}삭제됨!', delete_after=1) 
                    except:
                        await channel.send(f'{channel.name}삭제오류!') 
                        continue        
                await ctx.send('모든 채널 삭제완료!!', delete_after=1) 

            else:
                await ctx.channel.send('권한이 없습니다', delete_after=1)
        except Exception as e:
            print(e)

        
        

    # @commands.command(name='고양이')
    # async def prx_add(self, ctx: commands.Context):
    #     await self.cat_channel_del(ctx)

    @commands.hybrid_command ( name = '고양이', with_app_command = True,description="삭제 리스트에 있는 모든 채널을 청소합니다." )
    @commands.guild_only()
    async def add_with_app_command(self, ctx: commands.Context):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.cat_channel_del(ctx)

async def setup(bot):
    await bot.add_cog(Cat_del(bot), guilds=None) 