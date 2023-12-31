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
import yt_dlp
from discord import FFmpegPCMAudio

api_key ='AIzaSyDfcoQyQq2lcevMuF0_6sngn-8ww5d1M68'

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
def get_video_info(url: str):
    try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                video_info = ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as e:
            print(f"다운로드 오류: {e}")
            return None
    except yt_dlp.utils.ExtractorError as e:
            print(f"URL에서 정보 추출 오류: {e}")
            return None
    return video_info

def choose_best_audio(formats: list):
    audio_format = None
    for f in formats:
        if f['acodec'] != 'none' and (audio_format is None or f['abr'] > audio_format['abr']):
            audio_format = f
    return audio_format

class Loop_play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.volume = self.bot.vol_l


    async def l_play(self, ctx, file_name: str):
        if not str(ctx.guild.id) in self.bot.timer_runing:
            self.bot.timer_runing[str(ctx.guild.id)]=False

        if ctx.author.voice is None:
            await ctx.send("음성채널에 접속 하신 다음에 사용하셔야 하는 명령어 입니다.")
            return
        folder_path = "./sound"
        files = os.listdir(folder_path)
        new_file_name = None
        guild_id = str(ctx.guild.id)
        if guild_id not in self.volume:
            self.volume[str(ctx.guild.id)]=0.5
        client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
        db = client['music']
        collection = db[guild_id]
        song = collection.find_one({'name': file_name})
        FFMPEG_OPTIONS = {'options': '-vn'}
        
        if file_name.startswith('https://'or 'youtube'or 'www'):

            voice_channel = ctx.message.author.voice.channel
            if voice_channel is None:
                await ctx.send("음성 채널에 연결되어 있지 않습니다.")
                return
            video_info = get_video_info(file_name)
            if video_info is None:
                await ctx.send("유튜브 비디오 정보를 가져오는 도중 오류가 발생했습니다. 주소를 다시 확인해 주세요")
                return
            
            
            
            audio_format = choose_best_audio(video_info['formats'])
            audio_url = audio_format['url']
            audio_title = video_info['title']


            voice_client = ctx.voice_client
            FFMPEG_OPTIONS = {'options': '-vn'}
            # voice_client.play(FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS))
        elif song:
            
            u_name= song['url']
            video_info = get_video_info(u_name)
            if video_info is None:
                await ctx.send("유튜브 비디오 정보를 가져오는 도중 오류가 발생했습니다. 주소를 다시 확인해 주세요")
                return
            
            
            
            audio_format = choose_best_audio(video_info['formats'])
            audio_url = audio_format['url']
            audio_title = video_info['title']


        else:
            
            for file in files:
                name, extension = os.path.splitext(file)
                if name == file_name:
                    new_file_name = file
                    break

            if new_file_name is None:
                await ctx.channel.send(f"'{file_name}'이 없습니다. ``!음악목록``으로 리스트 확인해주세요\n추가원하시면 프리먼에게 문의")
                return

        try:
            channel = ctx.author.voice.channel
            voice = ctx.guild.voice_client

            if voice is None:
                voice = await channel.connect()

            if file_name.startswith('https://'or 'youtube'or 'www')or song is not None:
                source = discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS)
                await ctx.send(content=f"Now playing: {audio_title}",delete_after=2)
            else:
                source = discord.FFmpegPCMAudio(f"{folder_path}/{new_file_name}")

            
            while voice:
                if file_name.startswith('https://'or 'youtube'or 'www')or song is not None:
                    source = discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS)
                else:
                    source = discord.FFmpegPCMAudio(f"{folder_path}/{new_file_name}")
                voice.play(discord.PCMVolumeTransformer(source, self.volume[str(ctx.guild.id)]))
                while voice.is_playing():
                    await asyncio.sleep(1)

            if not self.bot.timer_runing[str(ctx.guild.id)]:
                await voice.disconnect()

        except Exception as e:
            await ctx.channel.send("재생중 오류발생")
            voice.stop()
            await voice.disconnect()
            print(e)




        
        

    # @commands.command(name='루프')
    # async def prx_add(self, ctx: commands.Context,file_name:str):
    #     await self.l_play(ctx,file_name)

    @commands.hybrid_command ( name = '루프', with_app_command = True,description="!멈춤 명령어를 쓸때까지 같은 음악을 연속 재생합니다." )
    @commands.guild_only()
    async def add_with_app_command(self, ctx: commands.Context,*,file_name:str):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)        
        await self.l_play(ctx,file_name)

async def setup(bot):
    await bot.add_cog(Loop_play(bot), guilds=None) 