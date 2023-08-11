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
import datetime

class Count_intimer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice = None
    async def timer(self, ctx: commands.Context, minutes: int):
        if not str(ctx.guild.id) in self.bot.timer_runing:
            self.bot.timer_runing[str(ctx.guild.id)]=False
        timer_running = self.bot.timer_runing[str(ctx.guild.id)]
        if not ctx.author.guild_permissions.administrator:
            await ctx.channel.send('권한이 없습니다', delete_after=1)
            return
        if ctx.author.voice is None:
            await ctx.channel.send("음성채널에 접속 하신 다음에 사용하셔야 하는 명령어 입니다.")
            return
        if timer_running:
            await ctx.channel.send("타이머가 이미 시작되어 있습니다.\n예기치 못한 상황에 종료되었을경우''!스탑업''명령어를 사용후 사용해 주세요")
            return

        self.bot.timer_runing[str(ctx.guild.id)] = True

        message = await ctx.channel.send('인타이머 시작!')
        member = ctx.guild.get_member(self.bot.user.id)
        channel = ctx.author.voice.channel
        if ctx.guild.voice_client is None:
            await channel.connect()
            # return
        # await channel.connect()
        member = ctx.guild.get_member(self.bot.user.id)
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(minutes=minutes)
        global ttcount
        ttcount = 0

        while self.bot.timer_runing[str(ctx.guild.id)] ==True:
            
            if self.bot.timer_runing[str(ctx.guild.id)] == False :
                print('인타이머 종료')
                break
            remaining = end_time - datetime.datetime.now()
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            remaining_string = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            if ttcount == 60:
                ttcount =0
            if ttcount == 0 and remaining.total_seconds() > 0:
                await member.edit(nick=f'⏰{remaining_string}')
            if remaining.total_seconds() < 0:
                await member.edit(nick=f'⏰시간종료!!')
                break
            await asyncio.sleep(1)
            
            ttcount +=1
            # await asyncio.sleep(60)

        self.bot.timer_runing[str(ctx.guild.id)] = False  
        embed1 = discord.Embed(colour=9999)
        embed1.add_field(name='타이머', value=f'```⏰ 지정시간이 되었습니다!!```', inline=True)
        
        await ctx.send(embed=embed1)
            
        await member.edit(nick=self.bot.oriname[str(ctx.guild.id)])
        if self.voice and not self.voice.is_playing():
                    
            await ctx.guild.voice_client.disconnect()
        
        

    # @commands.command(name='인타이머')
    # async def cmd_timer(self, ctx: commands.Context, minutes: int):
    #     await self.timer(ctx, minutes)

    @commands.hybrid_command ( name = '인타이머', with_app_command = True,description="음성 채널에서 지정된시간만큼 5초씩 차감되는 타이머 작동합니다." )
    @commands.guild_only()
    async def cmd_timer_with_app_command(self, ctx: commands.Context, minutes: int):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.timer(ctx, minutes)

async def setup(bot):
    await bot.add_cog(Count_intimer(bot), guilds=None) 
                