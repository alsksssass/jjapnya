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

class Loop_play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    async def l_play(self, ctx, file_name: str):
        if not ctx.author.guild_permissions.administrator:
            await ctx.channel.send('권한이 없습니다', delete_after=1)
            return
        guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
        channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
        await channel.send(f'{ctx.author.name}님이{ctx.guild.name}에서 음악루프 명령어 사용')
        folder_paths = ["./sound", f"./sound/{ctx.guild.id}"]
        new_file_name = None

        for folder_path in folder_paths:
            if not os.path.exists(folder_path):
                continue

            files = os.listdir(folder_path)

            for file in files:
                name, extension = os.path.splitext(file)
                if name == file_name:
                    new_file_name = name + extension
                    break

            if new_file_name:
                break

        if new_file_name is None:
            await ctx.channel.send(f"'{file_name}'이 없습니다. ``!음악목록``으로 리스트 확인해주세요\n추가원하시면!다운 명령어 사용.")
            return

        if ctx.author.voice is None:
            await ctx.channel.send("음성채널에 접속 하신 다음에 사용하셔야 하는 명령어 입니다.")
            return

        try:
            channel = ctx.author.voice.channel
            voice = ctx.guild.voice_client

            if voice is None:
                voice = await channel.connect()

            while voice:
                source = discord.FFmpegPCMAudio(f"{folder_path}/{new_file_name}")
                voice.play(source)
                while voice.is_playing():
                    await asyncio.sleep(1)

            # If the file is not found in any folder
            if new_file_name is None:
                await ctx.channel.send(f"'{file_name}'을(를) 찾을 수 없습니다.")
                return

        except Exception as e:
            await ctx.channel.send("재생중 오류발생")
            voice.stop()
            await voice.disconnect()
            print(e)



        
        

    @commands.command(name='루프')
    async def prx_add(self, ctx: commands.Context,file_name:str):
        await self.l_play(ctx,file_name)

    @commands.hybrid_command ( name = '루프_', with_app_command = True,description="!멈춤 명령어를 쓸때까지 같은 음악을 연속 재생합니다." )
    @commands.guild_only()
    async def add_with_app_command(self, ctx: commands.Context,file_name:str):
        await ctx.interaction.response.send_message(content='루프_명령어 사용됨',delete_after=0.000000001,ephemeral=True,silent=True)
        await self.l_play(ctx,file_name)

async def setup(bot):
    await bot.add_cog(Loop_play(bot), guilds=None) 