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

class Nick_del(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def del_nick(self,ctx,*args):
        if ctx.author.guild_permissions.administrator:
            a=args[0:]
            nick=' '.join(s for s in a)
            guild_id = str(ctx.guild.id)
            client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
            db = client['nickdatabase']
            collection = db[guild_id]

            # Get the guild ID
            guild_id = str(ctx.guild.id)

            # Get the collection for the guild
            collection = db[guild_id]

            # Extract the channel ID from the command
            channel_id = str(ctx.channel.id)

            # Delete the document with the matching channel ID
            result = collection.delete_one({'nick_name': nick})

            if result.deleted_count > 0:
                await ctx.channel.send(f'{nick}이(가) 삭제되었습니다!', delete_after=2)
            else:
                await ctx.channel.send(f'{nick}은 리스트에 존재하지 않습니다', delete_after=2)
        else:
                await ctx.channel.send('권한이 없습니다', delete_after=1)
    
    # @commands.command(name='닉제거')
    # async def prx(self,ctx: commands.Context,*args):
    #     await self.del_nick(ctx,*args)
                
    @commands.hybrid_command ( name = '닉제거', with_app_command = True,description="!캐릭터 에 들어갈 닉을 제거합니다." )
    @commands.guild_only()
    async def slash_with_app_command(self, ctx: commands.Context,*,닉):
            if hasattr(ctx, 'interaction') and ctx.interaction is not None:
                await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
            await self.del_nick(ctx,닉)
            
async def setup(bot):
    await bot.add_cog(Nick_del(bot), guilds=None)  # Add guild IDs if needed