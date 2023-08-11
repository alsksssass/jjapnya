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

class Nick_add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def add_nick(self,ctx,*,nick,roll=None):
        # Only respond to commands from users with the correct permissions
        if ctx.author.guild_permissions.administrator:
            guild_id = str(ctx.guild.id)
            client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
            db = client['nickdatabase']
            collection = db[guild_id]

            # db = client['mydatabase']
            # collection = db['channels']
            nick_string = ''.join(nick)
            
            # Check if the channel ID is already in the collection
            existing_channel = collection.find_one({'nick_name': nick_string})
            if existing_channel:
                
                await ctx.channel.send(f'{nick_string}은 이미 추가된 케릭터입니다', delete_after=2)
            else:
                
                # Insert a new document in the collection
                collection.insert_one({'nick_name': nick_string, 'roll': roll})
                if roll is None:
                    roll_name = '없음'
                else:
                    roll_name = roll
                await ctx.channel.send(f'{nick_string}이(가) 캐릭터 이름에 추가됨! 추가된 롤은{roll_name}입니다.', delete_after=2)
        else:
            await ctx.channel.send('권한이 없습니다', delete_after=1)
    
    # @commands.command(name='닉추가')
    # async def prx(self,ctx: commands.Context,*args):
    #     nick = ' '.join(args)
    #     # a=args[0:]
    #     # nick=''.join(s for s in a)
    #     await self.add_nick(ctx,nick)
        
                
    @commands.hybrid_command ( name = '닉추가', with_app_command = True,description="!캐릭터 에 들어갈 닉을 추가합니다." )
    @commands.guild_only()
    async def slash_with_app_command(self, ctx: commands.Context,*,닉,롤=None):
            if hasattr(ctx, 'interaction') and ctx.interaction is not None:
                await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
            await self.add_nick(ctx,nick=닉,roll=롤)
            
            
async def setup(bot):
    await bot.add_cog(Nick_add(bot), guilds=None)  # Add guild IDs if needed