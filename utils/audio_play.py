import discord
from discord.ext import commands
from discord.ui import Button, View,Select
import os
import pymongo
import asyncio
# from asyncio import sleep
import discord.utils
import yt_dlp
import random
import requests
import isodate
from mutagen import File, MutagenError
from utils.video_utils import get_video_info,choose_best_audio
# from pathlib import Path
# import urllib.request
# import urllib.error
import re
# import time
import traceback
# import logging
# import ffmpeg
# logging.basicConfig(level=logging.DEBUG)
import youtube_dl

YOUTUBE_API_KEY ='AIzaSyDfcoQyQq2lcevMuF0_6sngn-8ww5d1M68'
ydl_opts = {
'format': 'bestaudio/best',
'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'mp3',
    'preferredquality': '320',
}],
'logtostderr': True,
'extract_flat': True,
'skip_download': True,
'force-ipv4': True,
'cachedir': False,
}






async def on_button_click(self, url,guild_id):
    
    self.state='재생중'
    if url.startswith('http'):
        video_info = get_video_info(url)
        url2 = video_info['url']
        video_title = video_info['title']
    else:
        folder_path = f'./sound/{str(guild_id)}'
        url2=os.path.join(folder_path, url)
        video_title=url
    self.current_song[str(guild_id)]=url
    print(self.current_song[str(guild_id)])
    voice_state = interaction.user.voice
    # if interaction.response.is_done():
    #     print('asdss')
    # await interaction.response.send_message(f"재생 {video_title}", delete_after=0.5)
    try:
        await interaction.response.send_message(f"재생 {video_title}", delete_after=0.5)
    except:
        print('이미응답')
        await interaction.message.channel.send(f"재생 {video_title}", delete_after=0.5)
    # if not interaction.response.is_done:
    #     print('asd123')
    #     await interaction.message.channel.send(f"재생 {video_title}", delete_after=0.5)
    voice_channel = voice_state.channel
    try:# vc = await voice_channel.connect()
        if url.startswith('http'):
            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            audio_source = discord.FFmpegPCMAudio(url2, **FFMPEG_OPTIONS)
            print('asd6666')
        else:
            audio_source = discord.FFmpegPCMAudio(url2)
        print('asd11111')
        print('재생포인트')
        vc.play(discord.PCMVolumeTransformer(audio_source, self.volume[guild_id]))
    except Exception as e:
        print('dd>>')
        print(e)
        return
        # vc.play(discord.PCMVolumeTransformer(audio_source, self.volume[guild_id]))
    try:# await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
        embed= self.embed(title=None,file_path=f'./sound/{str(interaction.guild.id)}',guild_id=str(interaction.guild.id),name=str(interaction.user.global_name)or str(interaction.user.name))
    except:
        print('에러에러')
    try:
        print('정상수정')
        print(self.current_song[guild_id])
        # View 내의 컴포넌트들을 순회하며 Select 컴포넌트를 찾습니다.
        await interaction.message.edit(embed=embed)
    except:
        print('옵션수정')
        print(self.current_song[guild_id])
        channel = self.bot.get_channel(int(self.channel_id[guild_id][0]))
        message = await channel.fetch_message(int(self.msg[guild_id][0]))
        await message.edit(embed=embed) 
    # await interaction.message.edit(embed=embed,view=updated_components)  
# else:
#     print('asd????')
#     vc.play
while vc.is_playing():
    await asyncio.sleep(1)
# if vc.is_playing() or vc.is_paused():
#     pass

