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

class M_stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def stop_music(self,ctx):
        if ctx.author.guild_permissions.administrator:
            if not str(ctx.guild.id) in self.bot.timer_runing:
                self.bot.timer_runing[str(ctx.guild.id)]=False
            # Check if the bot is in a voice channel
            if ctx.guild.voice_client is None:
                await ctx.send("봇이 음성채널에 없습니다.")
                return
            
            if self.bot.timer_runing[str(ctx.guild.id)] == False:
                await ctx.guild.voice_client.disconnect()
                return
            elif self.bot.timer_runing[str(ctx.guild.id)] == True:
                ctx.guild.voice_client.stop()
                await ctx.guild.voice_client.disconnect()
                await asyncio.sleep(1)
                channel = ctx.author.voice.channel
                await channel.connect()

        else:
                await ctx.channel.send('권한이 없습니다', delete_after=1)
        
        

    # @commands.command(name='멈춤')
    # async def prx_add(self, ctx: commands.Context):
    #     await self.stop_music(ctx)

    @commands.hybrid_command ( name = '멈춤', with_app_command = True,description="플레이중인 음악을 멈춥니다." )
    @commands.guild_only()
    async def add_with_app_command(self, ctx: commands.Context):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.stop_music(ctx)

async def setup(bot):
    await bot.add_cog(M_stop(bot), guilds=None) 