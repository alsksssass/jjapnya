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
from discord import Thread
class Clean(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def clean_channel_del(self,ctx):
        if ctx.author.guild_permissions.administrator:
            channel_id=ctx.channel.id
            channel = self.bot.get_channel(int(channel_id))

            while True:
                messages = []
                async for message in channel.history(limit=99):
                    messages.append(message)
                    # await channel.delete_messages(messages)
                if not messages:
                    break
                
                await channel.purge(bulk=True)
            await ctx.channel.send(f'{ctx.channel.name}삭제됨!', delete_after=1)

        else:
            await ctx.channel.send('권한이 없습니다', delete_after=1)
        
        

    # @commands.command(name='청소')
    # async def prx_add(self, ctx: commands.Context):
    #     await self.clean_channel_del(ctx)

    @commands.hybrid_command ( name = '청소', with_app_command = True,description="현재 채널의 모든 메시지를 삭제합니다." )
    @commands.guild_only()
    async def add_with_app_command(self, ctx: commands.Context):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.clean_channel_del(ctx)

async def setup(bot):
    await bot.add_cog(Clean(bot), guilds=None) 