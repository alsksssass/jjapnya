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

class Stop_uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice = None

    
    async def stop_up(self,ctx):
        voice_state = self.bot.voice_client
        if ctx.author.guild_permissions.administrator:
            if not str(ctx.guild.id) in self.bot.timer_runing:
                self.bot.timer_runing[str(ctx.guild.id)]=False
            member = ctx.guild.get_member(self.bot.user.id)
            if self.bot.timer_runing[str(ctx.guild.id)] == False:
                await ctx.channel.send("타이머가 이미 중지되어 있습니다.")
                await member.edit(nick=self.bot.oriname[str(ctx.guild.id)])
                print(self.bot.timer_runing[str(ctx.guild.id)])
                return

            self.bot.timer_runing[str(ctx.guild.id)] = False
            await ctx.channel.send("타이머가 중지되었습니다.")
            await member.edit(nick=self.bot.oriname[str(ctx.guild.id)])
            print(self.bot.timer_runing[str(ctx.guild.id)])
            if voice_state:
                if voice_state.is_playing():
                    print('a')
                    
                else:
                    await ctx.guild.voice_client.disconnect()
                    print('b')
                    return
            
            # Wait 5 minutes before updating
        else:
                await ctx.channel.send('권한이 없습니다', delete_after=1)
    
    # @commands.command()
    # async def 스탑업(self,ctx: commands.Context):
    #     await self.stop_up(ctx)
                
    @commands.hybrid_command ( name = '스탑업', with_app_command = True,description="업타임을 종료합니다." )
    @commands.guild_only()
    async def 스탑업_with_app_command(self, ctx: commands.Context):
            if hasattr(ctx, 'interaction') and ctx.interaction is not None:
                await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
            await self.stop_up(ctx)
            
async def setup(bot):
    await bot.add_cog(Stop_uptime(bot), guilds=None)  # Add guild IDs if needed