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

EXCEL_EXTENSIONS = [".xlsx", ".xlsm", ".xlsb", ".xltx", ".xltm", ".xls", ".xlt", ".xla", ".xlw"]
MUSIC_EXTENSIONS = ['.mp3', '.wav', '.ogg']
class File_down(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def upload_file(self,ctx,sfile_name:str):
        if not ctx.author.guild_permissions.administrator:
            return await ctx.send('권한이 없습니다.')
        if not ctx.message.attachments:
            await ctx.send('명령어 쓴창에서 파일을 함께 업로드해주세요.')
            return

        guild_folder = f'./sound/{ctx.guild.id}/'
        cguild_folder = f'./dat/{ctx.guild.id}/'
        attachment = ctx.message.attachments[0]
        filetype = attachment.filename.split('.')[-1]
        print(filetype)
        acept=EXCEL_EXTENSIONS+MUSIC_EXTENSIONS
        print(acept)
        print(filetype)
        # 원하는 파일 형식(여기에서는 이미지 파일)로 제한
        if f'.{filetype}' not in acept:
            await ctx.send('지원하지 않는 파일 형식입니다. 이미지 파일만 제출해 주세요.')
            await ctx.send(f'지원하는 파일 형식은 {acept} 입니다.')
            return

        if f'.{filetype}' in EXCEL_EXTENSIONS:
            save_path = cguild_folder
            site_n='엑셀,데이터폴더'
        elif f'.{filetype}' in MUSIC_EXTENSIONS:
            save_path = guild_folder
            site_n='음악폴더'
        # 저장할 파일 이름 설정, 필요한 경우 다른 방식으로 설정
        save_filename = f'{sfile_name}.{filetype}'
        
        


        try:
            print(save_path)
            # 디렉토리가 없으면 생성합니다.
            os.makedirs(cguild_folder, exist_ok=True)
            os.makedirs(guild_folder, exist_ok=True)
            
            for file in os.listdir(guild_folder or cguild_folder):
                name, extension = os.path.splitext(file)
                if name == sfile_name:
                    return await ctx.send("같은 이름의 파일이 이미 있습니다.\n음악또는 엑셀파일과 이름이 같습니다.")

            # 파일을 저장합니다.
            save_filepath = os.path.join(save_path, save_filename)  # 저장 경로와 파일명을 결합합니다.
            await attachment.save(save_filepath)
            await ctx.send(f'{sfile_name}이름으로 파일이 {site_n}에 저장되었습니다')

        except Exception as e:
            await ctx.send(f'Error saving file: {e}')
            
        
    # async def module(self,ctx, sfile_name:str,url: str):
    #     if ctx.author.guild_permissions.administrator:
    #         # Get the guild's folder path
    #         guild_folder = f'./sound/{ctx.guild.id}/'
    #         cguild_folder = f'./dat/{ctx.guild.id}/'

    #         if not os.path.exists(guild_folder):
    #             os.makedirs(guild_folder)
    #         elif not os.path.exists(cguild_folder):
    #             os.makedirs(cguild_folder)

    #         # Get the file name from the URL
    #         file_name = os.path.basename(urlparse(url).path)
    #         print(file_name)
    #         ext = os.path.splitext(file_name)[1]
    #         save = sfile_name+ext

    #         chunk_size = 1024
    #         # Check if file with the same name exists
    #         # file_path = guild_folder + save
    #         # cfile_path = cguild_folder + save
    #         # if os.path.isfile(file_path) or os.path.isfile(cfile_path):
    #         #     await ctx.send("같은 이름의 파일이 이미 있습니다.")
    #         #     return
    #         for file in os.listdir(guild_folder or cguild_folder):
    #             name, extension = os.path.splitext(file)
    #             if name == sfile_name:
    #                 return await ctx.send("같은 이름의 파일이 이미 있습니다.\n 음악또는 엑셀파일과 이름이 같습니다.")
            
    #         # Check if the file extension is a music file extension
    #         if ext.lower() in MUSIC_EXTENSIONS:
    #             folder_name = "sound"
    #             response = requests.get(url)
    #             with open(f"{guild_folder}{save}", 'wb') as f:
    #                 # Iterate over the response content by chunk
    #                 for chunk in response.iter_content(chunk_size):
    #                     # Write the chunk to the file
    #                     f.write(chunk)
    #         # Check if the file extension is an Excel file extension
    #         elif ext.lower() in EXCEL_EXTENSIONS:
    #             folder_name = "clue"
    #             response = requests.get(url)
    #             with open(f"{cguild_folder}{save}", 'wb') as f:
    #                 # Iterate over the response content by chunk
    #                 for chunk in response.iter_content(chunk_size):
    #                     # Write the chunk to the file
    #                     f.write(chunk)
    #         else:
    #             await ctx.send("음악 파일 또는 엑셀 파일이 아닙니다.")
    #             return

    #         await ctx.send(f"{save} 이름으로 파일이 다운로드 되었습니다.")
    #         guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
    #         channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
    #         await channel.send(f'{ctx.author.name}님이{ctx.guild.name}에서 파일다운 명령어 사용')
    #     else:
    #         await ctx.channel.send('권한이 없습니다', delete_after=1)
    
    # @commands.command(name='파일다운')
    # async def prefix(self,ctx: commands.Context, sfile_name:str):
    #     await self.upload_file(ctx,sfile_name)
                
    @commands.hybrid_command ( name = '파일다운', with_app_command = True,description="!파일다운 으로만 사용해주세요.음악,엑셀파일을 길드에 저장합니다.(!개인,!로그 명령어로 불러옵니다.)" )
    @commands.guild_only()
    async def slash_with_app_command(self, ctx: commands.Context, *,저장할이름:str):
        sfile_name=저장할이름
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.upload_file(ctx,sfile_name)

    # @commands.command(name='다운파일')
    # async def prefix(self,ctx: commands.Context, sfile_name:str):
    #     await self.upload_file(ctx,sfile_name)

async def setup(bot):
    await bot.add_cog(File_down(bot), guilds=None)  # Add guild IDs if needed