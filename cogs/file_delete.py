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
class File_delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def module(self,ctx, filename: str):
        if ctx.author.guild_permissions.administrator:
            # Get the guild's folder path
            guild_folder = f'./sound/{ctx.guild.id}/'
            clue_folder = f'./dat/{ctx.guild.id}/'
            if not os.path.exists(guild_folder):
                await ctx.send("저장된 음악폴더가 없습니다.")
                return
            elif not os.path.exists(clue_folder):
                await ctx.send("저장된 엑셀폴더가 없습니다.")
                return

            file_paths = []
            for root, dirs, files in os.walk(guild_folder):
                for file in files:
                    name, extension = os.path.splitext(file)
                    if name == filename:
                        file_paths.append(os.path.join(root, file))

            for root, dirs, files in os.walk(clue_folder):
                for file in files:
                    name, extension = os.path.splitext(file)
                    if name == filename:
                        file_paths.append(os.path.join(root, file))

            if not file_paths:
                await ctx.send("파일을 찾을 수 없습니다.")
                return

            # Delete the files
            deleted_files = []
            for file_path in file_paths:
                os.remove(file_path)
                deleted_files.append(file_path)

            # Send a message to confirm the deletion
            await ctx.send(f"{len(deleted_files)}개의 파일이 삭제되었습니다:\n{deleted_files}")

    
        else:
            await ctx.channel.send('권한이 없습니다', delete_after=1)
    
    # @commands.command(name='파일삭제')
    # async def prefix(self,ctx: commands.Context, filename: str):
    #     await self.module(ctx,filename)
                
    @commands.hybrid_command ( name = '파일삭제', with_app_command = True,description="특정 음악,엑셀파일을 길드에서 삭제합니다." )
    @commands.guild_only()
    async def slash_with_app_command(self, ctx: commands.Context,*, filename: str):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.module(ctx,filename)
            
async def setup(bot):
    await bot.add_cog(File_delete(bot), guilds=None)  # Add guild IDs if needed