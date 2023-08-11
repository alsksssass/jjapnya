import discord
from discord import ui
from discord.ui import Button, View
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure, HybridCommand
import time
import os
import pymongo
from datetime import datetime, timedelta
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

class Del_num(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # async def De_channel(self,ctx, limit:int):
    #     if ctx.author.guild_permissions.administrator:
    #         if limit <= 0:
    #             await ctx.send('유효하지 않은 숫자입니다.')
    #             return

    #         await ctx.channel.purge(limit=limit, bulk=True)
    #         await ctx.send(f'{limit}개의 메시지가 삭제되었습니다.', delete_after=2)
    #         guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
    #         channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
    #         await channel.send(f'{ctx.author.name}님이{ctx.guild.name}에서 삭제명령어 사용')

            
    async def De_channel(self,ctx, limit:int, day:int):
        if 99 < limit <= 0 :
            await ctx.send('유효하지 않은 숫자입니다.')
            return
        # Retrieves the current date
        current_date = ctx.message.created_at

        # The timedelta object represents a duration of 15 days
        max_age = timedelta(days=day)

        # Prepare a check function to filter messages less than 15 days old
        def check(message):
            message_age = current_date - message.created_at
            return message_age < max_age

        # Retrieve the messages
        messages_to_delete = await ctx.channel.purge(limit=limit, check=check)

        # Send deletion confirmation message and delete it after 5 seconds
        status_message = await ctx.send(f'{len(messages_to_delete)}개의 메시지가 삭제되었습니다.!', delete_after=2)

    # @commands.command(name='삭제')
    # async def prx_add(self, ctx, num: int):
    #     if num <= 0:
    #             await ctx.send('유효하지 않은 숫자입니다.')
    #             return
    #     await ctx.channel.purge(limit=num+1, bulk=True)
    #     await ctx.send(f'{num}개의 메시지가 삭제되었습니다.', delete_after=2)

    @commands.hybrid_command ( name = '삭제', with_app_command = True,description="기입된 숫자만큼의 메시지 삭제." )
    @commands.guild_only()
    async def add_with_app_command(self, ctx: commands.Context, 숫자:int, day=15):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.De_channel(ctx, limit=숫자,day=day)
            

async def setup(bot):
    await bot.add_cog(Del_num(bot), guilds=None) 