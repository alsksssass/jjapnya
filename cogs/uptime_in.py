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

class In_uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.timer_running = timer_running
    async def in_uptimer(self,ctx: commands.Context):


        global timer_running
        if not str(ctx.guild.id) in self.bot.timer_runing:
            self.bot.timer_runing[str(ctx.guild.id)]=False
        timer_running = self.bot.timer_runing[str(ctx.guild.id)]
        if ctx.author.guild_permissions.administrator:
            
            if ctx.author.voice is None:
                await ctx.channel.send("음성채널에 접속 하신 다음에 사용하셔야 하는 명령어 입니다.")
                return
            if timer_running:
                await ctx.channel.send("타이머가 이미 시작되어 있습니다.\n예기치 못한 상황에 종료되었을경우''!스탑업''명령어를 사용후 사용해 주세요")
                return

            self.bot.timer_runing[str(ctx.guild.id)] = True
            ustart_time = datetime.now()
            message = await ctx.channel.send('업타임 시작!')
            member = ctx.guild.get_member(self.bot.user.id)
            channel = ctx.author.voice.channel
            if ctx.guild.voice_client is None:
                await channel.connect()
                # return print('11')
            # await member.guild.change_voice_state(channel=channel)
            print(self.bot.timer_runing[str(ctx.guild.id)])
            global ttcount
            ttcount = 0
            while self.bot.timer_runing[str(ctx.guild.id)] ==True:  # Update the message indefinitely
                current_time = datetime.now()
                elapsed_time = current_time - ustart_time
                elapsed_seconds = elapsed_time.total_seconds()
                elapsed_minutes, elapsed_seconds = divmod(elapsed_seconds, 60)
                elapsed_hours, elapsed_minutes = elapsed_minutes // 60, elapsed_minutes % 60

                # await message.edit(
                #     content=f'> 업타임 카운터\n```⏰플레이 하신지\n⏰{int(elapsed_hours):02d}시{int(elapsed_minutes):02d}분{int(elapsed_seconds):02d}초\n⏰지났습니다.```'
                # )  
                if ttcount == 60:
                    ttcount =0
                if ttcount == 0:
                    await member.edit(nick=f'{int(elapsed_hours):02d}시간{int(elapsed_minutes):02d}분{int(elapsed_seconds):02d}초')

                await asyncio.sleep(1)
            
                ttcount +=1


        else:
                await ctx.channel.send('권한이 없습니다', delete_after=1)
    
    # @commands.command()
    # async def 인업탐(self,ctx: commands.Context):
    #     await self.in_uptimer(ctx)
                
    @commands.hybrid_command ( name = '인업탐', with_app_command = True,description="사용직후부터 시간이 매분 업카운트 되는 타이머 작동 음성채팅방에 표시됨." )
    @commands.guild_only()
    async def 인업탐_with_app_command(self,ctx: commands.Context):
            if hasattr(ctx, 'interaction') and ctx.interaction is not None:
                await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
            await self.in_uptimer(ctx)
    
            
async def setup(bot):
    await bot.add_cog(In_uptime(bot), guilds=None)  # Add guild IDs if needed