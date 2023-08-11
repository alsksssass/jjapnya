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

class Count_timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def timer(self, ctx: commands.Context, minutes: int):
        try:
            if not ctx.author.guild_permissions.administrator:
                await ctx.channel.send('권한이 없습니다', delete_after=1)
                return
            start_time = datetime.datetime.now()
            end_time = start_time + datetime.timedelta(minutes=minutes)
            async def button_callback(interaction):
                user = interaction.user
                guild = interaction.guild
                member = await guild.fetch_member(user.id)
                if not member.guild_permissions.administrator:
                    await interaction.response.send_message(content='진행자만 진행이 가능합니다.',ephemeral=True)
                    return
                await interaction.message.delete()
            button_no = Button(label='종료', style=discord.ButtonStyle.red, custom_id=f'{ctx.guild.id}')
            buttons=[button_no]
            view = View(timeout=None)
            for value in buttons:
                value.callback = button_callback 
                view.add_item(value)
            message = await ctx.send('타이머 시작',view=view)

            while datetime.datetime.now() <= end_time:
                try:
                    remaining = end_time - datetime.datetime.now()
                    end_time_formatted = end_time.strftime('%I:%M:%S %p')
                    embed = discord.Embed(colour=9999)
                    embed.add_field(name='타이머', value=f'```⏰종료시간:{end_time_formatted}\n⏰{remaining.seconds // 60}분 {remaining.seconds % 60}초 남음\n종료는 메시지삭제. 타이머 초기화 메시지 뜬뒤에 다시 사용가능.```', inline=True)
                    await message.edit(embed=embed)
                    await asyncio.sleep(5)
                except Exception as e:
                    await ctx.channel.send('타이머 초기화됨', delete_after=1)
                    break
            
            embed1 = discord.Embed(colour=9999)
            embed1.add_field(name='타이머', value=f'```⏰ 지정시간이 되었습니다!!```', inline=True)
                    
            await message.edit(content='타이머 종료',embed=embed,delete_after=1)
            await ctx.channel.send(embed=embed1)
        except Exception as e:
            print(e)
    # @commands.command(name='타이머')
    # async def cmd_timer(self, ctx: commands.Context, minutes: int):
    #     await self.timer(ctx, minutes)

    @commands.hybrid_command ( name = '타이머', with_app_command = True,description="지정된시간만큼 5초씩 차감되는 타이머 작동합니다." )
    @commands.guild_only()
    async def cmd_timer_with_app_command(self, ctx: commands.Context, minutes: int):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.timer(ctx, minutes)

async def setup(bot):
    await bot.add_cog(Count_timer(bot), guilds=None) 
                