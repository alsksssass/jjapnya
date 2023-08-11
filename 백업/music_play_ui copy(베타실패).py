import discord
from discord.ext import commands
from discord import ui
from discord.ui import Button, View
import time
import os
import pymongo
from datetime import datetime
import asyncio
from asyncio import sleep
import json
import socket
import discord.utils
import yt_dlp
from discord import FFmpegPCMAudio
import random
import requests
import isodate
from collections import Counter
from urllib.parse import urlparse, parse_qs
from pydub import AudioSegment
import functools

YOUTUBE_API_KEY ='AIzaSyDfcoQyQq2lcevMuF0_6sngn-8ww5d1M68'
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
db = client['music']

def get_video_info1(url: str):
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

def get_video_info(url):
    YOUTUBE_API_KEY ='AIzaSyDfcoQyQq2lcevMuF0_6sngn-8ww5d1M68'
    video_id=url.replace('https://www.youtube.com/watch?v=', '')

    video_info_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={video_id}&key={YOUTUBE_API_KEY}"
    video_info_response = requests.get(video_info_url)
    video_info = video_info_response.json()["items"][0]
    content_details = video_info["contentDetails"]
    snippet = video_info["snippet"]

    video_duration = content_details["duration"]
    video_duration_seconds = int(isodate.parse_duration(video_duration).total_seconds())
    video_title = snippet['title']

    return {
        # 'url': f"https://www.youtube.com/watch?v={video_id}",
        'title': video_title,
        'duration': video_duration_seconds,
        'thumbnail': f"https://img.youtube.com/vi/{video_id}/0.jpg"
    }


class MusicControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playlists = []  # {guild_id: [song1_url, song2_url, ...]}
        self.repeat = None  # {guild_id: False}
        # self.volume = None
        self.volume = self.bot.vol_l# {guild_id: 1.0}
        self.current_song=None
        self.msg=''
        self.channel_id=''
        self.options = []
        self.playlists_1=[]
        self.state='대기중'
        self.music_list=[]
    class AddButton(discord.ui.Button):
        def __init__(self, bot,video_url,keyword, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.video_url = video_url
            self.keyword= keyword            
            self.bot = bot
            
        async def callback(self, interaction: discord.Interaction):
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("권한이 없습니다.", delete_after=1)
                return
            await interaction.response.send_message('처리중입니다.',delete_after=1)
            save_name=self.keyword
            # with yt_dlp.YoutubeDL() as ydl:
            #     info = ydl.extract_info(self.video_url, download=False)

            # video_url = info.get('webpage_url')
            # video_title = info.get('title')

            if interaction.user.guild_permissions.administrator:
                guild_id = str(interaction.guild.id)
                client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
                db = client['music']
                collection = db[guild_id]
                # db = client['mydatabase']
                # collection = db['channels']

                # Check if the channel ID is already in the collection
                existing_channel = collection.find_one({'name': save_name})
                if existing_channel:
                    await interaction.channel.send(f'{save_name}은 이미 추가어진 주소입니다.{self.video_url}', delete_after=2)

                else:

                    # Insert a new document in the collection
                    collection.insert_one({'name': save_name, 'url': self.video_url})
                    await interaction.channel.send(f'{save_name}이(가) 서버 유튜브 목록에 이름 추가됨!', delete_after=2)
            else:
                await interaction.channel.send('권한이 없습니다', delete_after=1)
    
    class AddButton1(discord.ui.Button):
        def __init__(self, bot,video_url,keyword, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.video_url = video_url
            self.keyword= keyword            
            self.bot = bot
            
        async def callback(self, interaction: discord.Interaction):
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("권한이 없습니다.", delete_after=1)
                return
            await interaction.response.send_message('처리중입니다.',delete_after=1)
            save_name=self.keyword
            # with yt_dlp.YoutubeDL() as ydl:
            #     info = ydl.extract_info(self.video_url, download=False)

            # video_url = info.get('webpage_url')
            # video_title = info.get('title')

            if interaction.user.guild_permissions.administrator:
                guild_id = str(interaction.user.id)
                client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
                db = client['music']
                collection = db[guild_id]
                # db = client['mydatabase']
                # collection = db['channels']

                # Check if the channel ID is already in the collection
                existing_channel = collection.find_one({'url': self.video_url})
                if existing_channel:
                    await interaction.channel.send(f'{save_name}은 이미 추가어진 주소입니다.{self.video_url}', delete_after=2)
                else:

                    # Insert a new document in the collection
                    collection.insert_one({'name': save_name, 'url': self.video_url})
                    await interaction.channel.send(f'{save_name}이(가) 개인유튜브 목록에 이름 추가됨!', delete_after=2)
            else:
                await interaction.channel.send('권한이 없습니다', delete_after=1)
                
    class ButtonExtend(discord.ui.View):
            def __init__(self, bot, video_url, keyword):
                super().__init__(timeout=None)
                self.add_item(MusicControl.AddButton1(bot,style=discord.ButtonStyle.grey, label=f"개인유튜브 리스트에 추가",
                                        custom_id=f"add_{video_url}1", video_url=video_url, keyword=keyword))
                self.add_item(MusicControl.AddButton(bot,style=discord.ButtonStyle.grey, label=f"서버유튜브 리스트에 추가",
                                        custom_id=f"add_{video_url}", video_url=video_url, keyword=keyword))

    class 삭제버튼(discord.ui.Button):
        def __init__(self, bot,ctx,index, collection, music_list, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.index = index
            self.collection = collection
            self.music_list = music_list
            self.bot=bot
            self.ctx=ctx
        async def callback(self, interaction: discord.Interaction):
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("권한이 없습니다.", delete_after=1)
                return
            await interaction.response.send_message(f"{self.index + 1} 번  항목이 삭제되었습니다!",delete_after=2)
            self.collection.delete_one({"name": self.music_list[self.index]["name"]})
            await interaction.message.delete()  # 이 부분을 추가하세요.

    async def on_button_click(self, interaction: discord.Interaction, button=None,track=None):
        try:
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("권한이 없습니다.", delete_after=1)
                return
            ctx = await self.bot.get_context(interaction.message)
            if button is None:
                button = interaction.data["custom_id"]
            if track is not None and button not in['개인유','서버유','개인','Next']:
                url = self.playlists[track]
                self.current_song = url
            else:
                if button in['개인유','서버유','개인','Next']:
                    pass
                else:
                    url = self.playlists[0]
                    self.current_song = url
            if button == "Play/Pause":
                voice_state = interaction.user.voice
                if voice_state is None:
                    await interaction.response.send_message('음성채널에 먼저 접속 하셔야 합니다.', delete_after=1)
                    return

                voice_channel = voice_state.channel
                vc = interaction.guild.voice_client or ctx.guild.voice_client
                if vc is None:
                    vc = await voice_channel.connect()
                if vc.is_playing():
                    vc.pause()
                    # self.current_song = None
                    self.state='일시정지'
                    await interaction.response.send_message('일시정지', delete_after=1)
                    # await self.music(ctx, rest=True,inuser_id=str(interaction.user.id))
                    return await self.music(ctx, rest=True,inuser_id=str(interaction.user.id))
                if vc.is_paused():
                    vc.resume()
                    # if not vc.is_playing():
                    #     return
                    # self.current_song = None
                    self.state='재생중'
                    await interaction.response.send_message('일시정지 해제', delete_after=1)
                    await self.music(ctx, rest=True,inuser_id=str(interaction.user.id))
                    return
                lis_mun=len(self.playlists)
                if lis_mun >0 :
                    self.state='재생중'
                    if url.startswith('http'):
                        info = get_video_info(url)
                        info1 = get_video_info1(url)
                        url2 = info1['url']
                        video_title = info['title']
                        
                    else:
                        folder_path = f'./sound/{str(interaction.guild.id)}'
                        url2=os.path.join(folder_path, url)
                        video_title=url
                    voice_state = interaction.user.voice
                    if interaction.response.is_done:
                        await interaction.response.send_message(f"재생 {video_title}", delete_after=1)
                    voice_channel = voice_state.channel
                    # vc = await voice_channel.connect()
                    if url.startswith('http'):
                        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
                        audio_source = discord.FFmpegPCMAudio(url2, **FFMPEG_OPTIONS)
                    else:
                        audio_source = discord.FFmpegPCMAudio(url2)
                    vc.play(discord.PCMVolumeTransformer(audio_source, self.volume))
                    await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
                else:
                    vc.play
                while vc.is_playing():
                    await asyncio.sleep(1)
                if not vc.is_playing() and vc.is_paused():
                    return 
                if self.repeat == '일반재생'and not vc.is_playing():
                    vc.stop()
                    self.state='정지1111'
                    await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
                    return
                elif self.repeat == '순차재생'and not vc.is_playing():
                    current_index = self.playlists.index(self.current_song)
                    if track == None and current_index + 1 < len(self.playlists):  # Check if there's a next song
                        index=current_index + 1
                        await self.play_next(interaction,index=index)
                        return
                elif self.repeat == '반복재생'and not vc.is_playing():
                    current_index = self.playlists.index(self.current_song)
                    await self.play_next(interaction,index=current_index)
                    return
                elif self.repeat == '셔플재생'and not vc.is_playing():
                    music_count = len(self.playlists)
                    if music_count > 1:
                        random_index = random.randint(0, music_count - 1)
                        index1 = random_index + 1
                    else:
                        index1 = 0
                    await self.play_next(interaction,index=index1)
                    return
                        
                else:
                    await ctx.send("플레이 리스트에 곡이 없습니다.", delete_after=1)
                    return
            
            elif button == "Stop":
                if interaction.guild.voice_client:
                    vc = interaction.guild.voice_client or ctx.guild.voice_client
                    if vc is None:
                        await interaction.response.send_message("음성채널에 없습니다.", delete_after=1)
                        return
                    elif vc.is_playing()or vc.is_paused:
                        vc.stop()
                        self.current_song = None
                        # await interaction.guild.voice_client.disconnect()
                        await interaction.response.send_message("정지", delete_after=1)
                        self.state='정지'
                        await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
                        return
                    else:
                        await interaction.response.send_message("플레이중이 아닙니다.", delete_after=1)
                        return
                else:
                    await interaction.response.send_message("플레이중이 아닙니다.", delete_after=1)
                    return
            elif button == "Next":
                current_index = self.playlists.index(self.current_song)
                if track == None and current_index + 1 < len(self.playlists):  # Check if there's a next song
                    await interaction.response.send_message("다음곡을 재생합니다.", delete_after=1)
                    index=current_index + 1
                    self.current_song=self.playlists[index]
                    await self.play_next(interaction,index=index)
                    return
                else:
                    await interaction.response.send_message("다음곡이 없습니다.", delete_after=1)
                    return
            elif button == "Repeat":
                if self.repeat == '일반재생':
                    self.repeat = '반복재생'
                    await interaction.response.send_message(f"재생모드가[{self.repeat}]로 변경되었습니다.", delete_after=1)
                    await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
                elif self.repeat == '반복재생':
                    self.repeat = '순차재생'
                    await interaction.response.send_message(f"재생모드가[{self.repeat}]로 변경되었습니다.", delete_after=1)
                    await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
                elif self.repeat == '순차재생':
                    self.repeat = '일반재생'
                    await interaction.response.send_message(f"재생모드가[{self.repeat}]로 변경되었습니다.", delete_after=1)
                    await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
            elif button == "Shuffle":
                self.repeat = '셔플재생'
                await interaction.response.send_message(f"재생모드가[{self.repeat}]로 변경되었습니다.", delete_after=1)
                await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
            elif button == "개인":
                if not interaction.user.guild_permissions.administrator:
                    await interaction.response.send_message("권한이 없습니다.", delete_after=1)
                    return
                await interaction.response.send_message(f"리스트가 폴더 리스트로 변경합니다.\n이 메시지가 사라지면 리스트가 변경완료 됩니다.", delete_after=1)
                folder_path = f'./sound/{str(interaction.guild.id)}'
                self.playlists=[]
                self.current_song = None
                allowed_extensions = ['.mp3', '.wav', '.ogg']
                # 폴더 내의 파일 이름 저장
                for file in os.listdir(folder_path):
                    file_extension = os.path.splitext(file)[1]
                    if file_extension in allowed_extensions:
                        self.playlists.append(file)
                await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
            elif button == "개인유":
                if not interaction.user.guild_permissions.administrator:
                    await interaction.response.send_message("권한이 없습니다.", delete_after=1)
                    return
                await interaction.response.send_message(f"리스트가 개인유튜브 리스트로 변경합니다.\n이 메시지가 사라지면 리스트가 변경완료 됩니다.", delete_after=1)
                collection = db[str(interaction.user.id)]
                self.playlists=[]
                self.current_song = None
                for doc in collection.find():
                    if 'url' in doc:
                        url = doc['url']
                        self.playlists.append(url)
                await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
                return
            elif button == "서버유":
                if not interaction.user.guild_permissions.administrator:
                    await interaction.response.send_message("권한이 없습니다.", delete_after=1)
                    return
                await interaction.response.send_message(f"리스트가 서버유튜브 리스트로 변경합니다.\n이 메시지가 사라지면 리스트가 변경완료 됩니다.", delete_after=1)
                self.current_song = None
                collection = db[str(interaction.guild.id)]
                self.playlists=[]
                for doc in collection.find():
                    if 'url' in doc:
                        url = doc['url']
                        self.playlists.append(url)
                await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
                return

        except Exception as e :
            if IndexError:
                await interaction.response.send_message("플레이리스트에 곡이 없습니다.\n리스트에 곡을 추가하고 해주세요!!!", delete_after=1)
                return
            print(e)
            await interaction.message.channel.send("{e}오류가 발생했습니다. 제작자에게 문의하세요!!", delete_after=1)
            return

    async def play_next(self, interaction,index=None):
        try:
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("권한이 없습니다.", delete_after=1)
                return
            ctx = await self.bot.get_context(interaction.message)
            if index is not None:
                if len(self.playlists)>0:
                    print('5647345')
                    self.state='재생중'
                    url = self.playlists[index]
                    # self.current_song = url
                    vc = interaction.guild.voice_client
                    if vc.is_playing():
                        vc.pause()
                    if url.startswith('http'):
                        info = get_video_info(url)
                        info1 = get_video_info1(url)
                        url2 = info1['url']
                        video_title = info['title']
                        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
                        audio_source = discord.FFmpegPCMAudio(url2, **FFMPEG_OPTIONS)
                    else:
                        folder_path = f'./sound/{str(interaction.guild.id)}'
                        url2=os.path.join(folder_path, url)
                        video_title=url
                        audio_source = discord.FFmpegPCMAudio(url2)
                    vc.play(discord.PCMVolumeTransformer(audio_source, self.volume))
                    await interaction.message.channel.send(f"재생 {video_title}", delete_after=1)
                    await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
                    while vc.is_playing():
                        await asyncio.sleep(1)
                    current_index = self.playlists.index(self.current_song)
                    if self.repeat == '일반재생':
                        vc.stop()
                        self.state='정지'
                        await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
                        return
                    elif self.repeat == '순차재생':
                        current_index = self.playlists.index(self.current_song)
                        if index == None and current_index + 1 < len(self.playlists):  # Check if there's a next song
                            index=current_index + 1
                            await self.play_next(interaction,index=index)
                            return
                        else:
                            self.state='음성채널에 없음'
                            vc.disconnect()
                            await interaction.message.channel.send("더이상 재생할 곡이 없습니다.", delete_after=1)
                            await self.music(ctx,rest=True)
                            return
                    elif self.repeat == '반복재생':
                        current_index = self.playlists.index(self.current_song)
                        await self.play_next(interaction,index=current_index)
                        return
                    elif self.repeat == '셔플재생':
                        music_count = len(self.playlists)
                        if music_count > 1:
                            random_index = random.randint(0, music_count - 1)
                            index = random_index + 1
                        await self.play_next(interaction,index=index)
                        return
                    else:
                        vc.disconnect()
                        self.state='음성채널에 없음'
                        await interaction.message.channel.send("더이상 재생할 곡이 없습니다.", delete_after=1)
                        await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
                        return
                else:
                    if interaction.guild.voice_client:
                        interaction.guild.voice_client.stop()
                        await interaction.guild.voice_client.disconnect()
                        self.state='음성채널에 없음'
                        await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
                        return
            else:
                # Here we send a message if there are no songs to play
                print("No songs to play")
                await interaction.message.channel.send("더이상 재생할 곡이 없습니다.", delete_after=1)
                # Or if you want to send a message to a specific channel:
                # channel = self.bot.get_channel(YOUR_CHANNEL_ID)
                # await channel.send("No songs to play")
        except Exception as e:
            print(e)
            await interaction.message.channel.send("{e}오류가 발생했습니다. 제작자에게 문의하세요!!", delete_after=1)


    async def select_callback(self, interaction: discord.Interaction):
        try:
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("권한이 없습니다.", delete_after=1)
                return
            ctx = await self.bot.get_context(interaction.message)
            song_url = interaction.data["values"]
            url=''.join(song_url)
            # await interaction.response.send_message("선택되엇습니다.")
            current_index = self.playlists.index(url)
            if song_url == "0":
                await interaction.response.send_message("리스트에 곡이 없습니다.", delete_after=1)
            else:
                voice_state = interaction.user.voice
                vc = ctx.guild.voice_client
                if vc is None:
                    pass
                else:
                    vc = interaction.guild.voice_client
                    if vc.is_playing():
                        vc.stop()
                    elif vc.is_paused():
                        vc.stop()
                    else:
                        vc.stop()
                # await ctx.send("재생할곡이 없습니다.", delete_after=1)
                await self.on_button_click(interaction, button="Play/Pause",track=current_index)


        except Exception as e:
            if not interaction.response.is_done:
                # No response has been sent yet
                await interaction.response.send_message("다시 선택해 주세요", delete_after=1)
            else:
                await interaction.message.channel.send('플레이할곡 선택을 대기합니다.', delete_after=1)
            print(e)
            await interaction.message.channel.send("{e}오류가 발생했습니다. 제작자에게 문의하세요!!", delete_after=1)
            # ydl_opts = {'format': 'bestaudio'}
            # with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            #     info = ydl.extract_info(url=song_url, download=False)
            #     url2 = info['url']
            #     video_title = info.get('title')
            #     thumbnail_url = info.get('thumbnail', None)
                
            #     voice_state = interaction.user.voice
            #     if voice_state is None or voice_state.channel is None:
            #         await interaction.response.send_message('음성채널에 먼저 접속 하셔야 합니다.')
            #         return
            #     voice_channel = voice_state.channel
            #     if interaction.guild.voice_client is None:
            #             vc = await voice_channel.connect()
            #     else:
            #         vc = interaction.guild.voice_client
            #     FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            #     audio_source = discord.FFmpegPCMAudio(url2, **FFMPEG_OPTIONS)
            #     vc.play(discord.PCMVolumeTransformer(audio_source, self.volume.get(interaction.guild.id)))
            #     voice_client = interaction.guild.voice_client
            #     await interaction.response.send_message(f"Playing {video_title}{thumbnail_url}")
            #     while vc.is_playing():
            #         await asyncio.sleep(1)
            #     await voice_client.disconnect()
            #     if interaction.guild.id in self.playlists and self.playlists[interaction.guild.id]:
            #         await self.play_next(interaction.guild)
            #     else:
            #         print("No songs to play")
                    # Or if you want to send a message to a specific channel:
                    # channel = self.bot.get_channel(YOUR_CHANNEL_ID)
                    # await channel.send("No songs to play")
                


    async def 찾기(self, ctx, keyword):
        youtube_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q={keyword}&type=video&key={YOUTUBE_API_KEY}"
        response = requests.get(youtube_url)
        results = response.json()["items"]
        
        for result in results:
            video_title = result["snippet"]["title"]
            video_id = result["id"]["videoId"]

            # Get the video duration
            video_info_url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={video_id}&key={YOUTUBE_API_KEY}"
            video_info_response = requests.get(video_info_url)
            video_info = video_info_response.json()["items"][0]["contentDetails"]
            video_duration = video_info["duration"]

            # Convert the video_duration to the "hh:mm:ss" format
            duration_timedelta = isodate.parse_duration(video_duration)
            hours, remainder = divmod(duration_timedelta.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_duration = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

            video_url = f"https://www.youtube.com/watch?v={video_id}"

            # Add the formatted_duration to the embed title
            embed = discord.Embed(title=f"{video_title} ({formatted_duration})", description=video_url, color=0x00ff00)

            playback_buttons = MusicControl.ButtonExtend(self.bot,video_url,keyword=video_title)
            msg = await ctx.send(embed=embed, view=playback_buttons)
    async def emulate_button(self, interaction, label):
        button = discord.ui.Button(style=discord.ButtonStyle.primary, label=label)
        await self.on_button_click(interaction, button)
        


        
    def convert_seconds_to_time_format(self,seconds=0):
        int_seconds = int(seconds)
        hours, remainder = divmod(int_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return time_str
    
    async def 목록(self, ctx,index):
        guild_id = str(index)
        db = self.bot.mongo['music']
        collection = db[guild_id]


        music_list = []
        
        for music in collection.find():
            music_list.append(music)
        e_msg=await ctx.send(f"{ctx.author.global_name}님의 유튜브 목록입니다.:")
        for index, music in enumerate(music_list):
            title = f"{index + 1}. {music['name']}"
            embed = discord.Embed(title=title, color=0x00ff00)
            bot=self.bot
            playback_buttons = discord.ui.View(timeout=None)
            playback_buttons.add_item(MusicControl.삭제버튼(label="삭제", custom_id=f"delete_{index}", ctx=ctx,bot=bot,index=index, collection=collection,music_list=music_list))
            # 다른 버튼을 추가하고 싶다면, 위와 비슷하게 여기에 추가하세요.
            
            msg = await ctx.send(embed=embed, view=playback_buttons)
        self.music_list=music_list

    # Assuming get_video_info() returns a dictionary with the key 'duration' holding the video duration in seconds
    async def embed(self,title=None,file_path=None):
        try:
            if self.current_song is None:
                embed=discord.Embed(title='타이틀', description=None, color=0xFF5733)
                embed.set_author(name="플레이 대기중", icon_url="https://i.imgur.com/VlKtyVf.png")
                embed.set_thumbnail(url="https://i.imgur.com/VlKtyVf.png")
                embed.add_field(name="노래길이", value=None, inline=True)
                embed.add_field(name="재생목록", value=None, inline=True)
                embed.add_field(name="볼륨", value=f'{(self.volume*100)}%', inline=True)
                embed.add_field(name="재생모드", value=self.repeat)
                embed.add_field(name="다음곡", value=None, inline=True)
                embed.set_footer(text="짭냥이플레이어 V 0.1", icon_url="https://i.imgur.com/VlKtyVf.png")
                return embed
            elif self.current_song is not  None:
                # if title is not None:
                #     duration_seconds = duration
                #     thumbnail_url = thunb
                #     title_name=title
                # else:
                if self.current_song.startswith('http'):
                    info = get_video_info(url=self.current_song)
                    # url2 = info['url']
                    video_title = info['title']
                    d_time = info['duration']
                    thumbnail_url = info['thumbnail']
                else:
                    if self.current_song in os.listdir(file_path):
                        file_path = os.path.join(file_path, self.current_song)

                        # Load the audio file using pydub and get its duration
                        audio = AudioSegment.from_file(file_path)
                        video_title = self.current_song
                        d_time = audio.duration_seconds
                        thumbnail_url='https://i.imgur.com/VlKtyVf.png'
                    else:
                        d_time=None
                state=self.state
                if self.repeat == '순차재생':
                    current_index = self.playlists.index(self.current_song)
                    if current_index + 1 < len(self.playlists):# Check if there's a next song
                        index=current_index + 1
                        current_index = self.playlists[index]
                        if current_index.startswith('http'):
                            next_info = get_video_info(url=current_index)
                            next_video_title = next_info['title']
                        else:
                            next_video_title = current_index
                    else:
                        next_video_title ='마지막 곡입니다.'
                if self.repeat == '셔플재생':
                    next_video_title ='랜덤재생'
                if self.repeat == '반복재생':
                    current_index = self.playlists.index(self.current_song)
                    # index=current_index
                    current_index = self.playlists[current_index]
                    if current_index.startswith('http'):
                        next_info = get_video_info(url=current_index)
                        next_video_title = next_info['title']
                    else:
                        next_video_title = current_index
                else:
                    next_video_title='없음'
                time_formatted = self.convert_seconds_to_time_format(seconds=d_time)
                embed=discord.Embed(title='타이틀', description=video_title, color=0xFF5733)
                embed.set_author(name=state, url="https://example.com", icon_url="https://i.imgur.com/VlKtyVf.png")
                embed.set_thumbnail(url=thumbnail_url)
                embed.add_field(name="노래길이", value=time_formatted, inline=True)
                embed.add_field(name="재생목록", value=len(self.playlists), inline=True)
                embed.add_field(name="볼륨", value=f'{(self.volume*100)}%', inline=True)
                embed.add_field(name="재생모드", value=self.repeat)
                embed.add_field(name="다음곡", value=next_video_title, inline=True)
                embed.set_footer(text="짭냥이플레이어 V 0.1", icon_url="https://i.imgur.com/VlKtyVf.png")
                return embed
        except Exception as e:
            print(e)
    async def set_volume(self, ctx, volume: float):
        if ctx.voice_client is None:
            return await ctx.send("봇이 음성 채널에 들어가지 않았습니다.")

        if 0 > volume > 100:
            return await ctx.send("음량을 0과 100 사이의 값으로 입력해주세요.")

        self.bot.vol_l = volume / 100
        if ctx.voice_client.is_playing():
            ctx.voice_client.source.volume = self.bot.vol_l

        await ctx.send(f"볼륨이 {volume}%로 조정되었습니다.")
    async def music(self, ctx,rest=False,inuser_id=None):
            try:
                guild_id=str(ctx.author.guild.id)
                if inuser_id is None:
                    user_id=str(ctx.author.id)
                else:
                    user_id=str(inuser_id)
                folder_path = f'./sound/{guild_id}'
                if self.repeat is None:
                    self.repeat = '일반재생'
                if len(self.playlists)>0:
                    self.options=[]
                    for url in self.playlists:
                        if url.startswith('http'):
                            info = get_video_info(url=url)
                            video_title = info.get('title')
                            self.options.append(discord.SelectOption(label=video_title, value=url))
                        else:
                            path=os.path.join(folder_path, url)
                            self.options.append(discord.SelectOption(label=url, value=url))
                elif len(self.playlists)==0:
                    self.options.append(discord.SelectOption(label="목록이 없습니다.", value="0"))
                if self.current_song is not None:
                    if self.current_song.startswith('http'):
                        info = get_video_info(url=self.current_song)
                        title = info['title']
                        place_name=f'재생중▶️{title}'
                        
                    else:
                        title = self.current_song
                        place_name=f'재생중▶️{self.current_song}'
                else:
                    place_name='곡을 선택해 주세요'
                components = [
                    discord.ui.Button(style=discord.ButtonStyle.primary, emoji="⏯️", custom_id='Play/Pause'),
                    discord.ui.Button(style=discord.ButtonStyle.primary, emoji="⏹️", custom_id='Stop'),
                    discord.ui.Button(style=discord.ButtonStyle.primary, emoji="⏭️", custom_id='Next'),
                    discord.ui.Button(style=discord.ButtonStyle.primary, emoji="🔁", custom_id='Repeat'),
                    discord.ui.Button(style=discord.ButtonStyle.primary, emoji="🔀", custom_id='Shuffle'),
                    discord.ui.Select(custom_id="select", placeholder=place_name, options=self.options,min_values=0)
                ]
                if os.path.isdir(folder_path):
                    components.append(discord.ui.Button(style=discord.ButtonStyle.primary, label='폴더',emoji="📁", custom_id='개인'))
                if guild_id in db.list_collection_names():
                    components.append(discord.ui.Button(style=discord.ButtonStyle.primary,label='서버', emoji="📁", custom_id='서버유'))
                if user_id in db.list_collection_names():
                    components.append(discord.ui.Button(style=discord.ButtonStyle.primary, label='개인',emoji="📁", custom_id='개인유'))
                view = View()
                for value in components:
                    if isinstance(value, discord.ui.Select):
                        value.callback = self.select_callback
                    else:
                        value.callback = self.on_button_click
                    view.add_item(value)


                embed=await self.embed(title=None,file_path=folder_path)
                if rest is False:
                    msg = await ctx.send(embed=embed, view=view)
                    self.msg=msg.id
                    self.channel_id=ctx.channel.id
                    return
                elif rest is True:
                    channel = self.bot.get_channel(self.channel_id)
                    message = await channel.fetch_message(self.msg)
                    await message.edit(embed=embed, view=view)
                    return
            except Exception as e:
                print(e)
        
    async def add_u_link(self,ctx,index,url:str):
        # Only respond to commands from users with the correct permissions
        guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
        channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
        await channel.send(f'{ctx.author.name}님이{ctx.guild.name}에서 유튜브 저장 명령어 사용')
        if ctx.author.guild_permissions.administrator:
            guild_id = str(index)
            client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
            db = client['music']
            collection = db[guild_id]
            video_info = get_video_info(url)
            info=video_info['title']
            # db = client['mydatabase']
            # collection = db['channels']

            # Check if the channel ID is already in the collection
            existing_channel = collection.find_one({'url': url})
            if video_info is None:
                await ctx.channel.send(f'주소가 정확하지 않습니다.', delete_after=2)
                return
            if existing_channel:
                await ctx.channel.send(f'{info}은 이미 추가되어 있습니다.', delete_after=2)
                return
            else:
                # Insert a new document in the collection
                collection.insert_one({'name': info, 'url': url, 'info': info})
                await ctx.channel.send(f'{info}이(가) 유튜브 목록에 추가됨!', delete_after=2)
                return
        else:
            await ctx.channel.send('권한이 없습니다', delete_after=1)
            return
    @commands.hybrid_command ( name = '검색', with_app_command = True,description="유튜브에서 음악을 검색함")
    @commands.guild_only()
    async def with_app_command1231222333(self, ctx: commands.Context,*,keyword):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
        channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
        await channel.send(f'{ctx.author.name}님이{ctx.guild.name}에서 검색 명령어 사용')
        await self.찾기(ctx,keyword=keyword)
    @commands.hybrid_command ( name = '귀여워', with_app_command = True,description="짭냥이플레이어를 실행합니다." )
    @commands.guild_only()
    async def with_app_command123123(self, ctx: commands.Context):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
        channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
        await channel.send(f'{ctx.author.name}님이{ctx.guild.name}에서 귀여워 명령어 사용')
        await self.music(ctx)
    @commands.hybrid_command ( name = '볼륨', with_app_command = True,description="봇의 음량을 조정합니다(1~99)값입력" )
    @commands.guild_only()
    async def 볼륨_with_app_command(self, ctx: commands.Context,volume: int):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
        channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
        await channel.send(f'{ctx.author.name}님이{ctx.guild.name}에서 볼륨 명령어 사용')
        await self.set_volume(ctx, volume)
            
    @commands.hybrid_command ( name = '개리업', with_app_command = True,description="개인유트브 음악목록을 표기함")
    async def with_app_command(self, ctx: commands.Context):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
                await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
        channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
        await channel.send(f'{ctx.author.name}님이{ctx.guild.name}에서 개리업 명령어 사용')
        index=ctx.author.id
        await self.목록(ctx,index=index)
    @commands.hybrid_command ( name = '서리업', with_app_command = True,description="서버유트브 음악목록을 표기함")
    @commands.guild_only()
    async def with_app_command1(self, ctx: commands.Context):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
                await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
        channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
        await channel.send(f'{ctx.author.name}님이{ctx.guild.name}에서 서리업 명령어 사용')
        index=ctx.guild.id
        await self.목록(ctx,index=index)
    @commands.hybrid_command ( name = '개인저장', with_app_command = True,description="!유트브 링크로 개인리스트에 저장합니다." )
    @commands.guild_only()
    async def slash_with_app_command122(self, ctx: commands.Context,url:str):
        m_name=ctx.author.id
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
        channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
        await channel.send(f'{ctx.author.name}님이{ctx.guild.name}에서 개저 명령어 사용')
        await self.add_u_link(ctx,m_name,url)
    @commands.hybrid_command ( name = '서버저장', with_app_command = True,description="!유트브 링크로 서버리스트에 저장합니다." )
    @commands.guild_only()
    async def slash_with_app_command1111(self, ctx: commands.Context,url:str):
        m_name=ctx.guild.id
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
        channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
        await channel.send(f'{ctx.author.name}님이{ctx.guild.name}에서 서저 명령어 사용')
        await self.add_u_link(ctx,m_name,url)
async def setup(bot):
    await bot.add_cog(MusicControl(bot))