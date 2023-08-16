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
from pydub import AudioSegment
from datetime import datetime
from discord.opus import Encoder
import os

YOUTUBE_API_KEY ='AIzaSyDfcoQyQq2lcevMuF0_6sngn-8ww5d1M68'
ydl_opts = {
'format': 'bestaudio/best',
'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'mp3',
    'preferredquality': '192',
}],
'logtostderr': True,
'extract_flat': True,
'skip_download': True,
'force-ipv4': True,
'cachedir': False,
}



# def is_url_playable(url: str) -> bool:
#     ydl_opts = {
#     'format': 'bestaudio/best',
#     'postprocessors': [{
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'mp3',
#         'preferredquality': '192',
#     }],
#     'logtostderr': True,
#     'extract_flat': True,
#     'skip_download': True,
#     'force-ipv4': True,
#     'cachedir': False,
#     }
    
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         try:
#             video_info = ydl.extract_info(url, download=False)
#             return True
#         except yt_dlp.utils.DownloadError:
#             return False
#         except yt_dlp.utils.ExtractorError:
#             return False

def check_audio_url_validity(url):
    try:
        response = requests.head(url)
        # response = requests.get(url, stream=True)
        if response.status_code == 200:
            return True
        else:
            response = requests.head(url)
            # response = requests.get(url, stream=True)
            if response.status_code == 200:
                return True
            else:
                return False
    except requests.exceptions.RequestException as e:
        return False

# def get_video_info(url: str):
#     while True:
#         try:
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 video_info = ydl.extract_info(url, download=False)
#             new_url=video_info['url']
#             if not check_audio_url_validity(new_url):
#                 print(f"URL '{url}' is not playable. Retrying...")
#                 continue
#             break
#         except yt_dlp.utils.DownloadError as e:
#             print('여기서 에러남7')
#             print(f"다운로드 오류: {e}")
#             return None
#         except yt_dlp.utils.ExtractorError as e:
#             print('여기서 에러남8')
#             print(f"URL에서 정보 추출 오류: {e}")
#             return None
#         except requests.exceptions.HTTPError as errh:
#             print('여기서 에러남1')

#     return video_info

# def get_video_info(url: str):
#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             video_info = ydl.extract_info(url, download=False)
#     # except Exception as e :
#     #     print(e)
#     #     print('dirdir;dir;11111')
#         url=video_info['url']
#     except yt_dlp.utils.DownloadError as e:
#             print('여기서 에러남7')
#             print(f"다운로드 오류: {e}")
#             return None
#     except yt_dlp.utils.ExtractorError as e:
#             print('여기서 에러남8')
#             print(f"URL에서 정보 추출 오류: {e}")
#             return None
#     except requests.exceptions.HTTPError as errh:
#         print('여기서 에러남1')
#     return video_info


def extract_video_id(url):
    video_id = re.search(r'(?:v=|/)([0-9A-Za-z_-]{11}).*', url)
    if video_id:
        return video_id.group(1)
    else:
        return None

def check_audio_url_validity(url):
    try:
        response = requests.head(url)
        # response = requests.get(url, stream=True)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False
# def get_video_info1(url):
#     try:
#         YOUTUBE_API_KEY ='AIzaSyDfcoQyQq2lcevMuF0_6sngn-8ww5d1M68'
#         video_id=extract_video_id(url=url)

#         video_info_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={video_id}&key={YOUTUBE_API_KEY}"
#         video_info_response = requests.get(video_info_url)
#         video_info_response.raise_for_status()

#         video_info = video_info_response.json()["items"][0]
#         content_details = video_info["contentDetails"]
#         snippet = video_info["snippet"]
#         video_duration = content_details["duration"]
#         video_duration_seconds = int(isodate.parse_duration(video_duration).total_seconds())
#         video_title = snippet['title']

#         return {
#             'title': video_title,
#             'duration': video_duration_seconds,
#             'thumbnail': f"https://img.youtube.com/vi/{video_id}/0.jpg"
#         }
#     except requests.exceptions.HTTPError as errh:
#         print ("Http Error:",errh)
#     except requests.exceptions.ConnectionError as errc:
#         print ("Error Connecting:",errc)
#     except requests.exceptions.Timeout as errt:
#         print ("Timeout Error:",errt)
#     except requests.exceptions.RequestException as err:
#         print ("Something went wrong",err)




def get_video_info1(url):
    YOUTUBE_API_KEY ='AIzaSyDfcoQyQq2lcevMuF0_6sngn-8ww5d1M68'
    video_id=extract_video_id(url=url)
    

    try:
        video_info_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={video_id}&key={YOUTUBE_API_KEY}"
        video_info_response = requests.get(video_info_url)
        video_info_response.raise_for_status()

        video_info = video_info_response.json()["items"][0]
        content_details = video_info["contentDetails"]
        snippet = video_info["snippet"]
        video_duration = content_details["duration"]
        video_duration_seconds = int(isodate.parse_duration(video_duration).total_seconds())
        video_title = snippet['title']
        return {
            'title': video_title,
            'duration': video_duration_seconds,
            'thumbnail': f"https://img.youtube.com/vi/{video_id}/0.jpg"
        }
    # except Exception as e :
    #     print(e)
    #     print('dirdir;dir;')
    except requests.exceptions.HTTPError as errh:
        print('여기서 에러남1')
        print ("Http Error:",errh) # wait for `backoff_in_seconds` seconds before next retry
    except requests.exceptions.ConnectionError as errc:
        print('여기서 에러남2')
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print('여기서 에러남3')
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print('여기서 에러남4')
        print ("Something went wrong",err)
            

    print("Failed to retrieve video info after retries.")
    return None






    
class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class VoiceClientRecorder:
        def __init__(self, client, output_filename):
            self.client = client
            self.output_filename = output_filename
            self.client._speaker_handlers[0] = self.on_speaker

        async def on_speaker(self, ss, user, data):
            with open(self.output_filename, 'ab') as f:
                f.write(data)

    async def pcm_to_mp3(self,pcm_path, mp3_path):
        audio = AudioSegment.from_file(pcm_path, format="raw", frame_rate=48000, channels=2, sample_width=2)
        audio.export(mp3_path, format="mp3")
    @commands.command(name='테스트')
    async def record(self,ctx):
        vc = ctx.author.voice

        if not vc:
            return await ctx.send('You\'re not in a voice channel.')

        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.channel.id != vc.channel.id:
            await voice_client.move_to(vc.channel)
        else:
            voice_client = await vc.channel.connect()

        def check_author(message):
            return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)

        await ctx.send(f'Recording started. Type `stop` to stop recording.')

        audio_files = []

        while True:
            try:
                message = await self.bot.wait_for('message', check=check_author, timeout=300)
                if message.content.lower() == 'stop':
                    break
                if message.attachments and message.attachments[0].filename.endswith(('.mp3', '.wav')):
                    audio_files.append(message.attachments[0])
                    print(audio_files)
            except asyncio.TimeoutError:
                break
        folder_name='test'
        save_path = os.path.join(os.getcwd(), folder_name)
        os.makedirs(save_path, exist_ok=True)
        print(audio_files)
        if audio_files:
            for index, audio_url in enumerate(audio_files):
                audio_data = await self.bot.http.get_audio(audio_url)
                file_name = f'record_{index + 1}.mp3'
                file_path = os.path.join(save_path, file_name)
                with open(file_path, 'wb') as f:
                    f.write(audio_data)

            await ctx.send(f'Recording stopped. Files saved in {save_path}')
        else:
            await ctx.send('No audio files were recorded.')

        await voice_client.disconnect()

async def setup(bot):
    await bot.add_cog(Testing(bot))