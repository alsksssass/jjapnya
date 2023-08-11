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

class Private_play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.volume = self.bot.vol_l


    async def p_play(self,ctx,file_name:str):
        if not ctx.author.guild_permissions.administrator:
            await ctx.channel.send('권한이 없습니다', delete_after=1)
            return
        if not str(ctx.guild.id) in self.bot.timer_runing:
            self.bot.timer_runing[str(ctx.guild.id)]=False
        folder_path = f"./sound/{ctx.guild.id}"
        files = os.listdir(folder_path)
        new_file_name = None  # 변수를 초기화합니다.
        for file in files:
            name, extension = os.path.splitext(file)
            if name == file_name:
                new_file_name = name + extension
                break  # 새 파일 이름을 찾은 경우 루프를 종료합니다.

        if new_file_name is None:
            await ctx.channel.send(f"'{file_name}'이 없습니다. ``!음악목록``으로 리스트 확인해주세요\n추가원하시면!파일다운 명령어 사용.")
            return

        if ctx.author.voice is None:
            await ctx.channel.send("음성채널에 접속 하신 다음에 사용하셔야 하는 명령어 입니다.")
            return
        guild_id=str(ctx.guild.id)
        if guild_id not in self.volume:
            self.volume[str(ctx.guild.id)]=0.5
        try:
            channel = ctx.author.voice.channel
            voice = ctx.guild.voice_client

            if voice is None:
                voice = await channel.connect()

            source = discord.FFmpegPCMAudio(f"{folder_path}/{new_file_name}")
            voice.play(discord.PCMVolumeTransformer(source, self.volume[str(ctx.guild.id)]))

            # 타이머가 실행 중인 경우
            if self.bot.timer_runing[str(ctx.guild.id)]:
                return

            # 타이머가 실행 중이지 않은 경우
            else:
                while voice.is_playing():
                    await sleep(1)
                await voice.disconnect()

        except Exception as e:
            await ctx.channel.send("재생중 오류발생")
            voice.stop()
            await voice.disconnect()
            print(e)
        
        

    # @commands.command(name='개인')
    # async def prx_add(self, ctx: commands.Context,file_name:str):
    #     await self.p_play(ctx,file_name)

    @commands.hybrid_command ( name = '개인', with_app_command = True,description="길드 전용 음악파일을 재생합니다." )
    @commands.guild_only()
    async def add_with_app_command(self, ctx: commands.Context,*,file_name:str):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.p_play(ctx,file_name)

async def setup(bot):
    await bot.add_cog(Private_play(bot), guilds=None) 