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

class Channel_list(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def list_channel_del(self,ctx):
        if ctx.author.guild_permissions.administrator:
                client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
                db = client['mydatabase']

                guild_id = str(ctx.guild.id)
                collection = db[guild_id]
                channels = collection.find({'guild_id': guild_id})
                channel_ids = collection.distinct('channel_id')

                channels = [self.bot.get_channel(int(id)) for id in channel_ids]
                
                # check if channel is not None before accessing name attribute
                channel_name_list = [f'{channel.name}\n' for channel in channels if channel is not None]
                
                # Remove None channels from DB
                for channel_id in channel_ids:
                    if self.bot.get_channel(int(channel_id)) is None:
                        collection.delete_one({'channel_id': channel_id})
                        

                result = ''.join(channel_name_list)
                channel_count = len(channel_name_list)
                
                await ctx.reply(f'삭제 채널 리스트 총 {channel_count} 개 :\n{result}', delete_after=10)
                guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
                channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
                await channel.send(f'{ctx.author.name}님이{ctx.guild.name}에서 채널리스트명령어 사용')
        else:
            await ctx.channel.send('권한이 없습니다', delete_after=1)
        
        



    @commands.hybrid_command ( name = '리스트', with_app_command = True,description="고양이 명령어로 삭제되는 채널 리스트를 확인합니다." )
    @commands.guild_only()
    async def add_with_app_command(self, ctx: commands.Context):
        await ctx.interaction.response.send_message(content='리스트_명령어 사용됨',delete_after=0.000000001,ephemeral=True,silent=True)
        await self.list_channel_del(ctx)

async def setup(bot):
    await bot.add_cog(Channel_list(bot), guilds=None) 