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

EXCEL_EXTENSIONS = {".xlsx", ".xlsm", ".xlsb", ".xltx", ".xltm", ".xls", ".xlt", ".xla", ".xlw"}
MUSIC_EXTENSIONS = ['.mp3', '.wav', '.ogg']
class File_show(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def module(self,ctx):
        if ctx.author.guild_permissions.administrator:
            # Get the guild's folder paths
            guild_folder = f'./sound/{ctx.guild.id}/'
            clue_folder = f'./dat/{ctx.guild.id}/'
            if not os.path.exists(guild_folder):
                await ctx.send("저장된 음악폴더가 없습니다.")
                return
            elif not os.path.exists(clue_folder):
                await ctx.send("저장된 엑셀폴더가 없습니다.")
                return

            # List files in each folder
            folder_names = ["음악 폴더", "엑셀 폴더"]
            folder_paths = [guild_folder, clue_folder]
            for folder_name, folder_path in zip(folder_names, folder_paths):
                file_list = []
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_list.append(os.path.join(root, file))

                if file_list:
                    file_list_str = "\n".join(file_list)
                    message = f"{folder_name}:\n{file_list_str}"
                    await ctx.send(message)
                else:
                    await ctx.send(f"{folder_name}에는 파일이 없습니다.")

        else:
            await ctx.channel.send('권한이 없습니다', delete_after=1)

    
    # @commands.command(name='파일보기')
    # async def prefix(self,ctx: commands.Context):
    #     await self.module(ctx)
                
    @commands.hybrid_command ( name = '파일보기', with_app_command = True,description="저장된 음악,엑셀파일들을 확인합니다." )
    @commands.guild_only()
    async def slash_with_app_command(self, ctx: commands.Context):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.module(ctx)
            
async def setup(bot):
    await bot.add_cog(File_show(bot), guilds=None)  # Add guild IDs if needed