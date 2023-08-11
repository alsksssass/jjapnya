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


class Gudock_add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



                
    @commands.hybrid_command ( name = '구독', with_app_command = True,description="업데이트 공지사항을 받습니다." )
    @commands.guild_only()
    async def slash_with_app_command(self, ctx: commands.Context):
            client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
            db = client['gudock']
            collection = db['list']
            if hasattr(ctx, 'interaction') and ctx.interaction is not None:
                await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
                    # Only respond to commands from users with the correct permissions

            if ctx.author.guild_permissions.administrator:

                nick=ctx.author.id
                
                existing_channel = collection.find_one({'user_id': nick})
                if existing_channel:
                    
                    await ctx.send(f'{ctx.author.global_name}님은 이미 구독중입니다', delete_after=2)
                else:
                    
                    # Insert a new document in the collection
                    collection.insert_one({'user_id': nick})
                    await ctx.send(f'{ctx.author.global_name}님을 공지구독 활성화 하였습니다.', delete_after=2)
                    guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
                    channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
                    await channel.send(f'{ctx.author.global_name}님 구독함')
            else:
                await ctx.channel.send('권한이 없습니다', delete_after=1)

    @commands.hybrid_command ( name = '서버제외', with_app_command = True,description="길드를 짭냥리스트에서 제외합니다." )
    @commands.guild_only()
    async def slash_with_app_command1(self, ctx: commands.Context):
            client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
            db = client['list_out']
            collection = db['list']
            if hasattr(ctx, 'interaction') and ctx.interaction is not None:
                await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
                    # Only respond to commands from users with the correct permissions
            guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
            channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
            await channel.send(f'{ctx.author.name}님이{ctx.guild.name}에서 구독 명령어 사용')
            if ctx.author.guild_permissions.administrator:

                guildid=ctx.guild.id
                
                existing_channel = collection.find_one({'guild_id': guildid})
                if existing_channel:
                    
                    await ctx.send(f'{ctx.guild.name}은 이미 제외되어 있습니다.', delete_after=2)
                else:
                    
                    # Insert a new document in the collection
                    collection.insert_one({'guild_id': guildid})
                    await ctx.send(f'{ctx.guild.name}을 제외 하였습니다.', delete_after=2)
                    guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
                    channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
                    await channel.send(f'{ctx.guild.name}서버 제외됨')
            else:
                await ctx.channel.send('권한이 없습니다', delete_after=1)

async def setup(bot):
    await bot.add_cog(Gudock_add(bot), guilds=None)  # Add guild IDs if needed