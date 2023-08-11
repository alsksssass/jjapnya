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
from .nick_chr import C_list
from .log1 import Log1

class Auto_s(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.c_list = C_list(bot)
        self.log1 = Log1(bot)
    # @commands.command(name='시작')
    async def my_command(self, ctx):
        print(self.bot.all_p)
        result = await self.c_list.show_list(ctx)#캐릭터선택
        while self.bot.all_p is False:#선택 완료시 진행
            await asyncio.sleep(1)
            print(self.bot.all_p)
            print(self.bot.player_l)
        if self.bot.all_p is True: #플레이 가능한거 확인되면 로그시작
            for user in self.bot.player_l:
                user_id = user[1]#유저id
                user_name = '플레이중'
                user = ctx.guild.get_member(user_id)
                role = discord.utils.get(ctx.guild.roles, name=user_name)
                await user.add_roles(role)#역할부여
            await self.log1.read_log(ctx,time_sc=1, file_name='대회장')
        while self.bot.all_p !='라운드1':#로그종료 대기
            await asyncio.sleep(1)
            print(self.bot.all_p)
        if self.bot.all_p == '라운드1':
            await ctx.send('1차조사 시작합니다. 단서 갯수는 x개 열람가능합니다. 2차조사때 사전조사가 필요한 단서가 있을수 있습니다.')
            await self.MyCog.버튼_s(ctx, order='1', num=30)
        while self.bot.all_p !='라운드2':#로그종료 대기
            await asyncio.sleep(1)
            print(self.bot.all_p)
        if self.bot.all_p == '라운드2':
            await ctx.send('2차조사 시작합니다. 단서 갯수는 x개 열람가능합니다.\n휴식이 필요하시면 조율하시고 휴식뒤에 진행하셔도 무방합니다.')
            await self.MyCog.버튼_s(ctx, order='1', num=30)
        while self.bot.all_p !='라운드3':#로그종료 대기
            await asyncio.sleep(1)
            print(self.bot.all_p)
        if self.bot.all_p == '라운드3':
            print(self.bot.all_p)
        
async def setup(bot):
    await bot.add_cog(Auto_s(bot), guilds=None)  # Add guild IDs if needed