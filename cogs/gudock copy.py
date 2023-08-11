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


class Gudock_del(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



            
                
    @commands.hybrid_command ( name = '구독취소', with_app_command = True,description="업데이트 공지 구독을 취소합니다." )
    @commands.guild_only()
    async def slash_with_app_command(self, ctx: commands.Context):
            client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
            db = client['gudock']
            collection = db['list']
            if hasattr(ctx, 'interaction') and ctx.interaction is not None:
                await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
            
            if ctx.author.guild_permissions.administrator:
                nick=ctx.author.id
                result = collection.delete_one({'user_id': nick})

                if result.deleted_count > 0:
                        await ctx.channel.send(f'{ctx.author.global_name}님은 구독 해제 되었습니다.', delete_after=2)
                else:
                        await ctx.channel.send(f'{ctx.author.global_name}님은 구독 리스트에 존재하지 않습니다', delete_after=2)
            else:
                    await ctx.channel.send('권한이 없습니다', delete_after=1)
    
    @commands.hybrid_command ( name = '서버추가', with_app_command = True,description="길드리스트에 다시 추가합니다." )
    @commands.guild_only()
    async def slash_with_app_command111(self, ctx: commands.Context):
            client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
            db = client['list_out']
            collection = db['list']
            if hasattr(ctx, 'interaction') and ctx.interaction is not None:
                await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
            
            if ctx.author.guild_permissions.administrator:
                guildid=ctx.guild.id
                result = collection.delete_one({'guild_id': guildid})

                if result.deleted_count > 0:
                        await ctx.channel.send(f'{ctx.guild.name}은 리스트에 다시 추가되었습니다..', delete_after=2)
                else:
                        await ctx.channel.send(f'{ctx.guild.name}은 서버 제외 리스트에 존재하지 않습니다', delete_after=2)
            else:
                    await ctx.channel.send('권한이 없습니다', delete_after=1)
            
async def setup(bot):
    await bot.add_cog(Gudock_del(bot), guilds=None)  # Add guild IDs if needed