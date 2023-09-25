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
        print ("Http Error:",errh) # wait for `backoff_in_seconds` seconds before next retry
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Something went wrong",err)
            

    print("Failed to retrieve video info after retries.")
    return None






    
class MusicControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playlists = {}  # {guild_id: [song1_url, song2_url, ...]}
        self.repeat = {} # {guild_id: False}
        # self.volume = None
        self.volume = self.bot.vol_l
        self.current_song={}
        self.msg={}
        self.channel_id={}
        self.components={}
        self.options = {}
        self.playlists_1={}
        self.state='대기중'
        self.music_list=[]
        self.shuffle_list={}
        self.file={}
        self.playing = {} # {guild_id: False}
    class AddButton(discord.ui.Button):
        def __init__(self, bot,video_url,keyword, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.video_url = video_url
            self.keyword= keyword            
            self.bot = bot

        # def add_song(self, guild_id=None, song_url=None):
        #     if guild_id!=None and song_url!=None:
        #         if guild_id not in self.playlists:
        #             self.playlists[guild_id] = []
        #         self.playlists[guild_id].append(song_url)
        #     else:
        #         return print('에드송에러')

        # # guild_id를 파라미터로 가지는 get_first_song 메서드
        # def get_first_song(self, guild_id=None):
        #     if guild_id!=None:
        #         if guild_id in self.playlists and len(self.playlists[guild_id]) > 0:
        #             return self.playlists[guild_id][0]
        #     else:
        #         return print('값에러')
        async def callback(self, interaction: discord.Interaction):
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("권한이 없습니다.", delete_after=0.5)
                return
            await interaction.response.send_message('처리중입니다.',delete_after=0.5)
            save_name=self.keyword
            # with yt_dlp.YoutubeDL() as ydl:
            #     info = ydl.extract_info(self.video_url, download=False)

            # video_url = info.get('webpage_url')
            # video_title = info.get('title')

            if interaction.user.guild_permissions.administrator:
                guild_id = str(str(interaction.guild.id))
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
                await interaction.channel.send('권한이 없습니다', delete_after=0.5)
    
    class AddButton1(discord.ui.Button):
        def __init__(self, bot,video_url,keyword, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.video_url = video_url
            self.keyword= keyword            
            self.bot = bot
            
        async def callback(self, interaction: discord.Interaction):
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("권한이 없습니다.", delete_after=0.5)
                return
            await interaction.response.send_message('처리중입니다.',delete_after=0.5)
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
                await interaction.channel.send('권한이 없습니다', delete_after=0.5)
                
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
                await interaction.response.send_message("권한이 없습니다.", delete_after=0.5)
                return
            await interaction.response.send_message(f"{self.index + 1} 번  항목이 삭제되었습니다!",delete_after=2)
            self.collection.delete_one({"name": self.music_list[self.index]["name"]})
            await interaction.message.delete()  # 이 부분을 추가하세요.

    async def on_button_click(self, interaction: discord.Interaction, button=None,track=None):
        try:
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("권한이 없습니다.", delete_after=0.5)
                return
            ctx = await self.bot.get_context(interaction.message)
            guild_id = str(interaction.guild.id)
            if button is None:
                button = interaction.data["custom_id"]
            if track is not None and button not in[f'{guild_id}개인유',f'{guild_id}서버유',f'{guild_id}개인',f'{guild_id}Next',f'{guild_id}disconnect']:
    
                url = self.playlists[str(interaction.guild.id)][track]
                self.current_song[str(interaction.guild.id)]=url
            else:
                if button in[f'{guild_id}개인유',f'{guild_id}서버유',f'{guild_id}개인',f'{guild_id}Next'f'{guild_id}stop',f'{guild_id}disconnect']:
                    pass
                # else:
                #     print('요기')
                #     url = self.playlists[str(interaction.guild.id)][0]
                #     # info = get_video_info(url)
                #     # video_title = info['title']
                #     self.current_song[str(interaction.guild.id)]=url
                #     print('요기')
            if button == f'{guild_id}Play/Pause':
                # await interaction.response.defer()
                voice_state = interaction.user.voice
                if voice_state is None:
                    await interaction.response.send_message('음성채널에 먼저 접속 하셔야 합니다.', delete_after=0.5)
                    return

                voice_channel = voice_state.channel
                vc = interaction.guild.voice_client or ctx.guild.voice_client
                if vc is None:
                    vc = await voice_channel.connect()
                if vc.is_playing():
                    self.state='일시정지'
                    print('일시정지')
                    vc.pause()
                    # self.current_song = None
                    await interaction.response.send_message('일시정지', delete_after=0.5)
                    # await self.music(ctx, rest=True,inuser_id=str(interaction.user.id))
                    embed= self.embed(title=None,file_path=f'./sound/{str(interaction.guild.id)}',guild_id=str(interaction.guild.id),name=str(interaction.user.global_name)or str(interaction.user.name))
                    try:
                        # View 내의 컴포넌트들을 순회하며 Select 컴포넌트를 찾습니다.
                        await interaction.message.edit(embed=embed)
                    except:
                        channel = self.bot.get_channel(int(self.channel_id[guild_id][0]))
                        message = await channel.fetch_message(int(self.msg[guild_id][0]))
                        await message.edit(embed=embed)
                    return
                if vc.is_paused():

                    vc.resume()
                    # if not vc.is_playing():
                    #     return
                    # self.current_song = None
                    self.state='재생중'
                    await interaction.response.send_message('일시정지 해제', delete_after=0.5)
                    embed= self.embed(title=None,file_path=f'./sound/{str(interaction.guild.id)}',guild_id=str(interaction.guild.id),name=str(interaction.user.global_name)or str(interaction.user.name))
                    try:
                        # View 내의 컴포넌트들을 순회하며 Select 컴포넌트를 찾습니다.
                        await interaction.message.edit(embed=embed)
                    except:
                        channel = self.bot.get_channel(int(self.channel_id[guild_id][0]))
                        message = await channel.fetch_message(int(self.msg[guild_id][0]))
                        await message.edit(embed=embed)
                    return
                # lis_mun=len(self.playlists[str(interaction.guild.id)])
                # if lis_mun >0 :
                else:
                    # vc.stop()
                    if vc.is_playing():
                        
                        return
                    if track is None and self.current_song[str(interaction.guild.id)] is None and self.repeat[str(interaction.guild.id)] != '셔플재생':
                        
                        url = self.playlists[str(interaction.guild.id)][0]
                    # elif self.repeat == '셔플재생':
                    #     random_index = random.randint(0, len(self.playlists[str(interaction.guild.id)]) - 1)
                    #     url = self.playlists[str(interaction.guild.id)][random_index]
                    else:
                        if track == None:
                            track=0
                        url = self.playlists[str(interaction.guild.id)][track]
                    self.state='재생중'
                    if url.startswith('http'):
                        # info1 = get_video_info(url)
                        # print(info1)
                        # url2 = info1['url']
                        # video_title = info1['title']
                        video_info = get_video_info(url)
                        # print(video_info)
                        # audio_format = choose_best_audio(video_info['formats'])
                        # print(audio_format)
                        url2 = video_info['url']
                        video_title = video_info['title']
                    else:
                        folder_path = f'./sound/{str(interaction.guild.id)}'
                        url2=os.path.join(folder_path, url)
                        video_title=url
                    self.current_song[str(interaction.guild.id)]=url
                    
                    voice_state = interaction.user.voice
                    # if interaction.response.is_done():
                    #     print('asdss')
                    # await interaction.response.send_message(f"재생 {video_title}", delete_after=0.5)
                    try:
                        await interaction.response.send_message(f"재생 {video_title}", delete_after=0.5)
                    except:
                        
                        await interaction.message.channel.send(f"재생 {video_title}", delete_after=0.5)
                    # if not interaction.response.is_done:
                    #     print('asd123')
                    #     await interaction.message.channel.send(f"재생 {video_title}", delete_after=0.5)
                    voice_channel = voice_state.channel
                    try:# vc = await voice_channel.connect()
                        if url.startswith('http'):
                            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
                            audio_source = discord.FFmpegPCMAudio(url2, **FFMPEG_OPTIONS)
                            
                        else:
                            audio_source = discord.FFmpegPCMAudio(url2)
                        
                        vc.play(discord.PCMVolumeTransformer(audio_source, self.volume[guild_id]))
                    except Exception as e:
                        
                        print(e)
                        return
                        # vc.play(discord.PCMVolumeTransformer(audio_source, self.volume[guild_id]))
                    try:# await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
                        embed= self.embed(title=None,file_path=f'./sound/{str(interaction.guild.id)}',guild_id=str(interaction.guild.id),name=str(interaction.user.global_name)or str(interaction.user.name))
                    except Exception as e:
                        print(e)
                    try:
                        # View 내의 컴포넌트들을 순회하며 Select 컴포넌트를 찾습니다.
                        await interaction.message.edit(embed=embed)
                    except:
                        channel = self.bot.get_channel(int(self.channel_id[guild_id][0]))
                        message = await channel.fetch_message(int(self.msg[guild_id][0]))
                        await message.edit(embed=embed) 
                    # await interaction.message.edit(embed=embed,view=updated_components)  
                # else:
                #     print('asd????')
                #     vc.play
                self.playing[str(guild_id)] = '재생'
                while vc.is_playing():
                    # if vc.stop():
                    #     self.playing[str(guild_id)] = '셀렉'
                    #     break
                    await asyncio.sleep(1)
                # vc.stop()
                # if vc.is_playing() or vc.is_paused():
                #     pass
                if self.repeat[str(interaction.guild.id)] == '일반재생'and not vc.is_paused()and self.playing[str(guild_id)] != '셀렉':
                    vc.stop()
                    self.state='정지'
                    # await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
                    embed= self.embed(title=None,file_path=f'./sound/{str(interaction.guild.id)}',guild_id=str(interaction.guild.id),name=str(interaction.user.global_name)or str(interaction.user.name))
                    try:
                        # View 내의 컴포넌트들을 순회하며 Select 컴포넌트를 찾습니다.
                        await interaction.message.edit(embed=embed)
                    except:
                        channel = self.bot.get_channel(int(self.channel_id[guild_id][0]))
                        message = await channel.fetch_message(int(self.msg[guild_id][0]))
                        await message.edit(embed=embed)
                    return
                elif self.repeat[str(interaction.guild.id)] == '순차재생'and not vc.is_paused()and self.playing[str(guild_id)] != '셀렉':
                    if self.current_song[str(interaction.guild.id)] != None:
                        current_index = self.playlists[str(interaction.guild.id)].index(self.current_song[str(interaction.guild.id)])
                    else:
                        current_index=0
                    if current_index + 1 >= len(self.playlists[str(interaction.guild.id)]):  # Check if there's a next song
                        current_index= 0
                    else:
                        current_index += 1
                    # await self.play_next(interaction,index=current_index)
                    await self.on_button_click(interaction,button=f'{guild_id}Play/Pause',track=current_index)
                    return
                elif self.repeat[str(interaction.guild.id)] == '반복재생'and not vc.is_paused()and self.playing[str(guild_id)] != '셀렉':
                    current_index = self.playlists[str(interaction.guild.id)].index(self.current_song[str(interaction.guild.id)])
                    # await self.play_next(interaction,index=current_index)
                    await self.on_button_click(interaction,button=f'{guild_id}Play/Pause',track=current_index)
                    return
                elif self.repeat[str(interaction.guild.id)] == '셔플재생'and not vc.is_paused()and self.playing[str(guild_id)] != '셀렉':
                    if self.current_song[str(interaction.guild.id)] == None:
                        index_s=0
                        self.current_song[str(interaction.guild.id)]=self.shuffle_list[str(interaction.guild.id)][0]
                        current_index=0
                    else:
                        index_s=self.shuffle_list[str(interaction.guild.id)].index(self.current_song[str(interaction.guild.id)])
                        if index_s+1>=len(self.shuffle_list[str(interaction.guild.id)]):
                            index_s=0
                        else:
                            index_s+=1
                        shuffle11=self.shuffle_list[str(interaction.guild.id)][index_s]
                        current_index = self.playlists[str(interaction.guild.id)].index(shuffle11)
                        
                    await self.on_button_click(interaction,button=f'{guild_id}Play/Pause',track=current_index)
                    return
                elif vc.is_paused():
                    pass
                else:
                    # await ctx.send("플레이 리스트에 곡이 없습니다.", delete_after=0.5)
                    return
            
            elif button == f'{guild_id}Stop':
                if interaction.guild.voice_client:
                    vc = interaction.guild.voice_client or ctx.guild.voice_client
                    if vc is None:
                        await interaction.response.send_message("음성채널에 없습니다.", delete_after=0.5)
                        return
                    self.state='정지'
                    if guild_id not in self.volume:
                            self.volume[str(ctx.guild.id)]=0.5
                    elif vc.is_playing()or vc.is_paused:
                        await interaction.response.send_message("정지", delete_after=0.5)
                        original_volume = self.volume[str(ctx.guild.id)]
                        time_step = 3 / 100
                        volume_step = original_volume / 100
                        for step in range(100, -1, -1):
                            await asyncio.sleep(time_step)
                            vc.source.volume = volume_step * step
                        vc.stop()
                        self.current_song[str(interaction.guild.id)]=None
                        try:
                            embed= self.embed(title=None,file_path=f'./sound/{str(interaction.guild.id)}',guild_id=str(interaction.guild.id),name=str(interaction.user.global_name)or str(interaction.user.name))
                            # View 내의 컴포넌트들을 순회하며 Select 컴포넌트를 찾습니다.
                            await interaction.message.edit(embed=embed)
                        except:
                            channel = self.bot.get_channel(int(self.channel_id[guild_id][0]))
                            message = await channel.fetch_message(int(self.msg[guild_id][0]))
                            await message.edit(embed=embed)
                        return
                    else:
                        await interaction.response.send_message("플레이중이 아닙니다.", delete_after=0.5)
                        return
                else:
                    await interaction.response.send_message("플레이중이 아닙니다.", delete_after=0.5)
                    return
            elif button == f'{guild_id}Next':
                if self.current_song[str(interaction.guild.id)]!=None:
                    ctx = await self.bot.get_context(interaction.message)
                    voice_state = interaction.user.voice
                    voice_channel = voice_state.channel
                    vc = interaction.guild.voice_client or ctx.guild.voice_client
                    if vc is None:
                        pass
                    else:
                        if vc.is_playing():
                            vc.stop()
                        elif vc.is_paused():
                            vc.stop()
                        else:
                            vc.stop()
                    await interaction.response.send_message("다음곡", delete_after=0.5)
                    # current_index = self.playlists[str(interaction.guild.id)].index(self.current_song[str(interaction.guild.id)])
                    # print(len(self.playlists[str(interaction.guild.id)]))
                    # # if track == None and current_index + 1 >= len(self.playlists[str(interaction.guild.id)]) and self.repeat != '셔플재생':  # Check if there's a next song
                    # #     current_index=0
                    # # else:
                    # #     current_index+=1
                    # # name=self.playlists[str(interaction.guild.id)][current_index]
                    # # if interaction.response.is_done:
                    # #     print('asdss')
                    # #     try:
                    # #         await interaction.response.send_message(f"다음곡 재생", delete_after=0.5)
                    # #     except:
                    # #         await interaction.message.channel.send(f"다음곡 재생", delete_after=0.5)
                    # # self.current_song[str(interaction.guild.id)]=name
                    if self.repeat[str(interaction.guild.id)] == '일반재생':
                        current_index = self.playlists[str(interaction.guild.id)].index(self.current_song[str(interaction.guild.id)])
                        if current_index + 1 >= len(self.playlists[str(interaction.guild.id)]):  # Check if there's a next song
                            current_index= 0
                        else:
                            current_index += 1
                        # await self.play_next(interaction,index=current_index)
                        await self.on_button_click(interaction,button=f'{guild_id}Play/Pause',track=current_index)
                        return
                    # elif self.repeat == '순차재생':
                    #     print('다음재생에서 순차재생')
                    #     current_index = self.playlists[str(interaction.guild.id)].index(self.current_song[str(interaction.guild.id)])
                    #     print(f'{current_index}기본번호')
                    #     if current_index + 1 >= len(self.playlists[str(interaction.guild.id)]):  # Check if there's a next song
                    #         current_index= 0
                    #         print('0으로')
                    #     else:
                    #         print('다음으로')
                    #         current_index += 1
                    #     print('순차재생')
                    #     print(current_index)
                    #     # await self.play_next(interaction,index=current_index)
                    #     await self.on_button_click(interaction,button=f'{guild_id}Play/Pause',track=current_index)
                    #     return
                    # elif self.repeat == '반복재생':
                    #     print('다음재생에서 반복재생')
                    #     print('반복재생')
                    #     current_index = self.playlists[str(interaction.guild.id)].index(self.current_song[str(interaction.guild.id)])
                    #     # await self.play_next(interaction,index=current_index)
                    #     await self.on_button_click(interaction,button=f'{guild_id}Play/Pause',track=current_index)
                    #     return
                    # elif self.repeat == '셔플재생':
                    #     print('다음재생에서 셔플재생')
                    #     print('셔플재생')
                    #     if self.current_song[str(interaction.guild.id)] == None:
                    #         index_s=0
                    #         self.current_song[str(interaction.guild.id)]=self.shuffle_list[str(interaction.guild.id)][0]
                    #         current_index=0
                    #     else:
                    #         index_s=self.shuffle_list[str(interaction.guild.id)].index(self.current_song[str(interaction.guild.id)])
                    #         if index_s+1>=len(self.shuffle_list[str(interaction.guild.id)]):
                    #             index_s=0
                    #         else:
                    #             index_s+=1
                    #         shuffle11=self.shuffle_list[str(interaction.guild.id)][index_s]
                    #         current_index = self.playlists[str(interaction.guild.id)].index(shuffle11)
                            
                    #     await self.on_button_click(interaction,button=f'{guild_id}Play/Pause',track=current_index)
                    #     return
                    # # if self.repeat == '셔플재생':
                    # #     index_s=self.shuffle_list[str(interaction.guild.id)].index(self.current_song[str(interaction.guild.id)])
                    # #     if index_s+1>=len(self.shuffle_list[str(interaction.guild.id)]):
                    # #         index_s=0
                    # #     else:
                    # #         index_s+=1
                    # #     shuffle11=self.shuffle_list[str(interaction.guild.id)][index_s]
                    # #     current_index = self.playlists[str(interaction.guild.id)].index(shuffle11)
                    # #     print(len(self.playlists[str(interaction.guild.id)]))
                    # #     if track == None and current_index + 1 >= len(self.playlists[str(interaction.guild.id)]):  # Check if there's a next song
                    # #         current_index=0
                    # #     else:
                    # #         current_index+=1
                        
                    # # # await self.play_next(interaction,index=current_index)
                    # # await self.on_button_click(interaction,button=f'{guild_id}Play/Pause',track=current_index)
                    # return

                # elif self.current_song[str(interaction.guild.id)] is None:
                #     if not interaction.response.is_done:
                #         await interaction.response.send_message("다음곡을 재생합니다.", delete_after=0.5)
                #     self.current_song[str(interaction.guild.id)]=self.playlists[str(interaction.guild.id)][0]
                #     # await self.play_next(interaction,index=0)
                #     await self.on_button_click(interaction,button=f'{guild_id}Play/Pause',track=0)
                #     return
                # else:
                #     await interaction.response.send_message("다음곡이 없습니다.", delete_after=0.5)
                #     return
            elif button == f'{guild_id}Repeat':
                if self.repeat[str(interaction.guild.id)] == '일반재생':
                    self.repeat[str(interaction.guild.id)] = '반복재생'
                    await interaction.response.send_message(f"재생모드가[{self.repeat[str(interaction.guild.id)]}]로 변경되었습니다.", delete_after=0.5)
                    # await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
                    embed= self.embed(title=None,file_path=f'./sound/{str(interaction.guild.id)}',guild_id=str(interaction.guild.id),name=str(interaction.user.global_name)or str(interaction.user.name))
                    try:
                        # View 내의 컴포넌트들을 순회하며 Select 컴포넌트를 찾습니다.
                        await interaction.message.edit(embed=embed)
                    except:
                        channel = self.bot.get_channel(int(self.channel_id[guild_id][0]))
                        message = await channel.fetch_message(int(self.msg[guild_id][0]))
                        await message.edit(embed=embed)
                    return
                elif self.repeat[str(interaction.guild.id)] == '반복재생':
                    self.repeat[str(interaction.guild.id)] = '순차재생'
                    await interaction.response.send_message(f"재생모드가[{self.repeat[str(interaction.guild.id)]}]로 변경되었습니다.", delete_after=0.5)
                    # await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
                    embed= self.embed(title=None,file_path=f'./sound/{str(interaction.guild.id)}',guild_id=str(interaction.guild.id),name=str(interaction.user.global_name)or str(interaction.user.name))
                    try:
                        # View 내의 컴포넌트들을 순회하며 Select 컴포넌트를 찾습니다.
                        await interaction.message.edit(embed=embed)
                    except:
                        channel = self.bot.get_channel(int(self.channel_id[guild_id][0]))
                        message = await channel.fetch_message(int(self.msg[guild_id][0]))
                        await message.edit(embed=embed)
                    return
                elif self.repeat[str(interaction.guild.id)] == '순차재생':
                    self.repeat[str(interaction.guild.id)] = '일반재생'
                    await interaction.response.send_message(f"재생모드가[{self.repeat[str(interaction.guild.id)]}]로 변경되었습니다.", delete_after=0.5)
                    embed= self.embed(title=None,file_path=f'./sound/{str(interaction.guild.id)}',guild_id=str(interaction.guild.id),name=str(interaction.user.global_name)or str(interaction.user.name))
                    try:
                        # View 내의 컴포넌트들을 순회하며 Select 컴포넌트를 찾습니다.
                        await interaction.message.edit(embed=embed)
                    except:
                        channel = self.bot.get_channel(int(self.channel_id[guild_id][0]))
                        message = await channel.fetch_message(int(self.msg[guild_id][0]))
                        await message.edit(embed=embed)
                    return
                elif self.repeat[str(interaction.guild.id)] == '셔플재생':
                    self.repeat[str(interaction.guild.id)] = '일반재생'
                    await interaction.response.send_message(f"재생모드가[{self.repeat[str(interaction.guild.id)]}]로 변경되었습니다.", delete_after=0.5)
                    # await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
                    embed= self.embed(title=None,file_path=f'./sound/{str(interaction.guild.id)}',guild_id=str(interaction.guild.id),name=str(interaction.user.global_name)or str(interaction.user.name))
                    try:
                        # View 내의 컴포넌트들을 순회하며 Select 컴포넌트를 찾습니다.
                        await interaction.message.edit(embed=embed)
                    except:
                        channel = self.bot.get_channel(int(self.channel_id[guild_id][0]))
                        message = await channel.fetch_message(int(self.msg[guild_id][0]))
                        await message.edit(embed=embed)
                    return
            elif button == f'{guild_id}Shuffle':
                self.repeat[str(interaction.guild.id)] = '셔플재생'
                if len(self.playlists[str(interaction.guild.id)])<0:
                    await interaction.response.send_message(f"리스트를 추가하고 눌러주세요", delete_after=0.5)
                else:
                    if str(interaction.guild.id) in self.shuffle_list:
                        self.shuffle_list[interaction.guild.id] =[]
                    self.shuffle_list[str(interaction.guild.id)] = self.playlists[str(interaction.guild.id)][:]
                    random.shuffle(self.shuffle_list[str(interaction.guild.id)])
                    await interaction.response.send_message(f"재생모드가[{self.repeat[str(interaction.guild.id)]}]로 변경되었습니다.", delete_after=0.5)
                    # await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
                    embed= self.embed(title=None,file_path=f'./sound/{str(interaction.guild.id)}',guild_id=str(interaction.guild.id),name=str(interaction.user.global_name)or str(interaction.user.name))
                    try:
                        # View 내의 컴포넌트들을 순회하며 Select 컴포넌트를 찾습니다.
                        await interaction.message.edit(embed=embed)
                    except:
                        channel = self.bot.get_channel(int(self.channel_id[guild_id][0]))
                        message = await channel.fetch_message(int(self.msg[guild_id][0]))
                        await message.edit(embed=embed)
                    return
            elif button == f'{guild_id}개인':
                folder_path = f'./sound/{str(interaction.guild.id)}'
                if not interaction.user.guild_permissions.administrator:
                    await interaction.response.send_message("권한이 없습니다.", delete_after=0.5)
                    return
                if not os.path.isdir(folder_path):
                    await interaction.response.send_message(f"{interaction.user.name}님은 개인폴더가 없습니다.", delete_after=0.5)
                    return
                elif not os.listdir(folder_path):
                    await interaction.response.send_message(f"{interaction.user.name}님의 폴더에 파일이 없습니다.", delete_after=0.5)
                    return
                await interaction.response.send_message(f"리스트가 폴더 리스트로 변경합니다.\n이 메시지가 사라지면 리스트가 변경완료 됩니다.", delete_after=1)

                self.file[guild_id] = '폴더'
                folder_path = f'./sound/{str(str(interaction.guild.id))}'
                # self.playlists=[]
                self.playlists[guild_id]=[]
                if not str(interaction.guild.id) in self.current_song:
                    self.current_song[str(interaction.guild.id)] = None
                elif str(interaction.guild.id) in self.current_song and self.current_song[str(interaction.guild.id)] not in self.playlists[guild_id]:
                    self.current_song[str(interaction.guild.id)] = None
                allowed_extensions = ['.mp3', '.wav', '.ogg']
                # 폴더 내의 파일 이름 저장
                for file in os.listdir(folder_path):
                    file_extension = os.path.splitext(file)[1]
                    if file_extension in allowed_extensions:
                        # self.playlists.append(file)
                        self.playlists[str(interaction.guild.id)].append(file)
                self.playlists[guild_id].sort()
                await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
                # embed= self.embed(title=None,file_path=f'./sound/{str(interaction.guild.id)}',guild_id=str(interaction.guild.id),name=str(interaction.user.global_name)or str(interaction.user.name))
                # await interaction.message.edit(embed=embed)
            elif button == f'{guild_id}개인유':
                client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
                db = client['music']
                if not interaction.user.guild_permissions.administrator:
                    await interaction.response.send_message("권한이 없습니다.", delete_after=0.5)
                    return
                if not str(interaction.user.id) in db.list_collection_names():
                    await interaction.response.send_message(f"{interaction.user.name}님은 개인 유튜브 저장 폴더가 없습니다.", delete_after=0.5)
                    return
                await interaction.response.send_message(f"리스트가 개인유튜브 리스트로 변경합니다.\n이 메시지가 사라지면 리스트가 변경완료 됩니다.", delete_after=1)
                
                self.file[guild_id] = '개인유튜브'
                
                collection = db[str(interaction.user.id)]
                # self.playlists=[]
                self.playlists[guild_id]=[]
                if not str(interaction.guild.id) in self.current_song:
                    self.current_song[str(interaction.guild.id)] = None
                elif str(interaction.guild.id) in self.current_song and self.current_song[str(interaction.guild.id)] not in self.playlists[guild_id]:
                    self.current_song[str(interaction.guild.id)] = None
                for doc in collection.find():
                    if 'url' in doc:
                        url = doc['url']
                        video_id=extract_video_id(url=url)
                        new_url=f"https://www.youtube.com/watch?v={video_id}"
                        # self.playlists.append(url)
                        self.playlists[str(interaction.guild.id)].append(new_url)
                await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
                # embed= self.embed(title=None,file_path=f'./sound/{str(interaction.guild.id)}',guild_id=str(interaction.guild.id),name=str(interaction.user.global_name)or str(interaction.user.name))
                # await interaction.message.edit(embed=embed)
                return
            elif button == f'{guild_id}서버유':
                client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
                db = client['music']
                if not interaction.user.guild_permissions.administrator:
                    await interaction.response.send_message("권한이 없습니다.", delete_after=0.5)
                    return
                if not str(interaction.guild.id) in db.list_collection_names():
                    await interaction.response.send_message(f"{interaction.guild.name}에는 서버 유튜브 저장 폴더가 없습니다.", delete_after=0.5)
                    return
                await interaction.response.send_message(f"리스트가 서버유튜브 리스트로 변경합니다.\n이 메시지가 사라지면 리스트가 변경완료 됩니다.", delete_after=1)

                self.file[guild_id] = '서버유튜브'
                collection = db[str(interaction.guild.id)]
                # self.playlists=[]
                self.playlists[guild_id]=[]
                if not str(interaction.guild.id) in self.current_song:
                    self.current_song[str(interaction.guild.id)] = None
                elif str(interaction.guild.id) in self.current_song and self.current_song[str(interaction.guild.id)] not in self.playlists[guild_id]:
                    self.current_song[str(interaction.guild.id)] = None
                for doc in collection.find():
                    if 'url' in doc:
                        url = doc['url']
                        video_id=extract_video_id(url=url)
                        new_url=f"https://www.youtube.com/watch?v={video_id}"
                        # self.playlists.append(url)
                        self.playlists[str(interaction.guild.id)].append(new_url)
                await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
                # embed= self.embed(title=None,file_path=f'./sound/{str(interaction.guild.id)}',guild_id=str(interaction.guild.id),name=str(interaction.user.global_name)or str(interaction.user.name))
                # await interaction.message.edit(embed=embed)
                return
            elif button == f'{guild_id}disconnect':
                if not interaction.user.guild_permissions.administrator:
                    await interaction.response.send_message("권한이 없습니다.", delete_after=0.5)
                    return
                await interaction.response.send_message("플레이어 종료합니다.", delete_after=0.5)
                voice_state = interaction.user.voice
                vc = interaction.guild.voice_client or ctx.guild.voice_client
                if vc is not None:
                    voice_channel = voice_state.channel
                    # if vc.is_playing() or vc.is_paused()or vc.stop():
                    #     print('왓냐??')
                    await vc.disconnect()
                await interaction.message.delete()

                self.playlists[guild_id]=[]
                self.options[guild_id]=[]
                self.current_song[guild_id]=None
                self.components[guild_id]=[]
                self.msg[guild_id] = []
                self.channel_id[guild_id]=[]

                return

        except Exception as e :
            traceback.print_exc()
            print(e)
            

    # async def play_next(self, interaction,index=None):
    #     try:
    #         if not interaction.user.guild_permissions.administrator:
    #             await interaction.response.send_message("권한이 없습니다.", delete_after=0.5)
    #             return
    #         ctx = await self.bot.get_context(interaction.message)
    #         if index is not None:
    #             if len(self.playlists[str(interaction.guild.id)])>0:
    #                 self.state='재생중'
    #                 if self.repeat == '셔플재생':
    #                     url = self.shuffle_list[str(interaction.guild.id)][index]
    #                 else:
    #                     url = self.playlists[str(interaction.guild.id)][index]
    #                 # self.current_song = url
    #                 voice_state = interaction.user.voice
    #                 voice_channel = voice_state.channel
    #                 vc = interaction.guild.voice_client
    #                 if vc is None:
    #                     vc = await voice_channel.connect()
    #                 if vc.is_playing():
    #                     vc.pause()
    #                 if url.startswith('http'):
    #                     self.current_song[str(interaction.guild.id)]=url
    #                     info = get_video_info(url)
    #                     info1 = get_video_info(url)
    #                     url2 = info1['url']
    #                     video_title = info['title']
    #                     FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    #                     audio_source = discord.FFmpegPCMAudio(url2, **FFMPEG_OPTIONS)
    #                 else:
    #                     self.current_song[str(interaction.guild.id)]=url
    #                     folder_path = f'./sound/{str(str(interaction.guild.id))}'
    #                     url2=os.path.join(folder_path, url)
    #                     video_title=url
    #                     audio_source = discord.FFmpegPCMAudio(url2)
    #                 vc.play(discord.PCMVolumeTransformer(audio_source, self.volume[str(interaction.guild.id)]))
    #                 if interaction.response.is_done:
    #                     await interaction.response.send_message(f"재생 {video_title}", delete_after=0.5)
    #                 if not interaction.response.is_done:
    #                     await interaction.message.channel.send(f"재생 {video_title}", delete_after=0.5)
    #                 await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
    #                 while vc.is_playing():
    #                     await asyncio.sleep(1)
    #                 current_index = self.playlists[str(interaction.guild.id)].index(self.current_song[str(interaction.guild.id)])
    #                 if self.repeat == '일반재생':
    #                     vc.stop()
    #                     self.state='정지'
    #                     await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
    #                     return
    #                 elif self.repeat == '순차재생':
    #                     current_index = self.playlists[str(interaction.guild.id)].index(self.current_song[str(interaction.guild.id)])
    #                     if index == None and current_index + 1 >= len(self.playlists[str(interaction.guild.id)]):  # Check if there's a next song
    #                         current_index=0
    #                     else:
    #                         current_index+=1
    #                     await self.play_next(interaction,index=current_index)
    #                     await self.music(ctx,rest=True)
    #                     return
    #                 elif self.repeat == '반복재생':
    #                     current_index = self.playlists[str(interaction.guild.id)].index(self.current_song[str(interaction.guild.id)])
    #                     await self.play_next(interaction,index=current_index)
    #                     await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
    #                     return
    #                 elif self.repeat == '셔플재생':
    #                     index_s=self.shuffle_list[str(interaction.guild.id)].index(self.current_song[str(interaction.guild.id)])
    #                     if index_s+1>=len(self.shuffle_list[str(interaction.guild.id)]):
    #                         index_s=0
    #                     else:
    #                         index_s+=1
    #                     await self.play_next(interaction,index=(index_s))
    #                     await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
    #                     return
    #                 else:
    #                     await vc.disconnect()
    #                     self.state='음성채널에 없음'
    #                     await interaction.message.channel.send("더이상 재생할 곡이 없습니다.", delete_after=0.5)
    #                     await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
    #                     return
    #             else:
    #                 if interaction.guild.voice_client:
    #                     interaction.guild.voice_client.stop()
    #                     await interaction.guild.voice_client.disconnect()
    #                     self.state='음성채널에 없음'
    #                     await self.music(ctx,rest=True,inuser_id=str(interaction.user.id))
    #                     return
    #         else:
    #             # Here we send a message if there are no songs to play
    #             print("No songs to play")
    #             await interaction.message.channel.send("더이상 재생할 곡이 없습니다.", delete_after=0.5)
    #             # Or if you want to send a message to a specific channel:
    #             # channel = self.bot.get_channel(YOUR_CHANNEL_ID)
    #             # await channel.send("No songs to play")
    #     except Exception as e:
    #         if IndexError:
    #             print(e)
    #         print(e)


    async def select_callback(self, interaction: discord.Interaction):
        try:
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("권한이 없습니다.", delete_after=0.5)
                return
            guild_id=str(interaction.guild.id)
            self.playing[str(guild_id)] = '셀렉'
            ctx = await self.bot.get_context(interaction.message)
            song_url = interaction.data["values"]
            url=''.join(song_url)
            # print(interaction.data['components'])
            # await interaction.response.send_message("선택되엇습니다.")
            current_index = self.playlists[str(interaction.guild.id)].index(url)
            
            if song_url == "0":
                await interaction.response.send_message("리스트에 곡이 없습니다.", delete_after=0.5)
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
                # await ctx.send("재생할곡이 없습니다.", delete_after=0.5)
                await self.on_button_click(interaction, button=f'{guild_id}Play/Pause',track=current_index)


        except Exception as e:
            traceback.print_exc()
            print(e)
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
            #     vc.play(discord.PCMVolumeTransformer(audio_source, self.volume.get(str(interaction.guild.id))))
            #     voice_client = interaction.guild.voice_client
            #     await interaction.response.send_message(f"Playing {video_title}{thumbnail_url}")
            #     while vc.is_playing():
            #         await asyncio.sleep(1)
            #     await voice_client.disconnect()
            #     if str(interaction.guild.id) in self.playlists and self.playlists[str(interaction.guild.id)]:
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
    
    async def 목록(self, ctx,index,title=None):
        guild_id = str(index)
        db = self.bot.mongo['music']
        collection = db[guild_id]


        music_list = []
        
        for music in collection.find():
            music_list.append(music)
        if title == '개인':
            e_msg=await ctx.send(f"{ctx.author.global_name}님의 유튜브 목록입니다.:")
        else:
            e_msg=await ctx.send(f"{ctx.guild.name}의 유튜브 목록입니다.:")
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
    def embed(self,title=None,file_path=None,guild_id=None,name=None):
        try:
            if guild_id in self.file:
                file_name=self.file[guild_id]
            elif guild_id not in self.file:
                file_name='없음'
            if guild_id in self.playlists:
                num=len(self.playlists[guild_id])
            elif guild_id not in self.playlists:
                num=0
            if self.current_song[guild_id]==None:
                embed=discord.Embed(title='타이틀', description=None, color=0xFF5733)
                embed.set_author(name="플레이 대기중", icon_url="https://i.imgur.com/Eze649t.gif")
                embed.set_thumbnail(url="https://i.imgur.com/Eze649t.gif")
                embed.add_field(name="노래길이", value=None, inline=True)
                embed.add_field(name="재생목록", value=f'{file_name}의{num}개음악', inline=True)
                embed.add_field(name="볼륨", value=f'{(self.volume[guild_id]*100)}%', inline=True)
                embed.add_field(name="재생모드", value=self.repeat[str(guild_id)])
                embed.add_field(name="다음곡", value=None, inline=True)
                embed.add_field(name="조작자", value=name, inline=True)
                embed.set_footer(text="짭냥이플레이어 V 0.30", icon_url="https://i.imgur.com/VlKtyVf.png")
                return embed
            elif self.current_song[guild_id]!=None:
                # if title is not None:
                #     duration_seconds = duration
                #     thumbnail_url = thunb
                #     title_name=title
                # else:
                if self.current_song[guild_id].startswith('http'):
                    try:
                        info = get_video_info1(url=str(self.current_song[guild_id]))
                        if info == None:
                            info = get_video_info(url=str(self.current_song[guild_id]))
                        # url2 = info['url']
                        video_title = info['title']
                        d_time = info['duration']
                        thumbnail_url = info['thumbnail']
                    except :
                        traceback.print_exc()
                else:
                    if self.current_song[guild_id] in os.listdir(file_path):
                        file_path = os.path.join(file_path, self.current_song[guild_id])

                        try:# Load the audio file using pydub and get its duration
                            audio = File(file_path)
                            video_title = self.current_song[guild_id]
                            # d_time = audio.duration_seconds
                            d_time = audio.info.length
                            thumbnail_url='https://i.imgur.com/MwovhA7.gif'
                        except MutagenError:  # 예외가 발생하면 0을 반환합니다.
                            video_title = self.current_song[guild_id]
                            d_time=0
                            thumbnail_url='https://i.imgur.com/MwovhA7.gif'
                state=self.state
                if self.repeat[str(guild_id)] == '순차재생':
                    index_s=self.playlists[guild_id].index(self.current_song[guild_id])
                    if index_s+1>=len(self.playlists[guild_id]):
                        index_s=0
                    else:
                        index_s += 1
                    index_name=self.playlists[guild_id][index_s]
                    if index_name.startswith('http'):
                        next_info = get_video_info1(url=index_name)
                        if next_info==None:
                            next_info = get_video_info(url=index_name)
                        next_video_title = next_info['title']
                    else:
                        next_video_title = index_name
                if self.repeat[str(guild_id)] == '셔플재생':
                    index_s=self.shuffle_list[guild_id].index(self.current_song[guild_id])
                    if index_s+1>=len(self.shuffle_list[guild_id]):
                        index_s=0
                    else:
                        index_s += 1
                    index_name=self.shuffle_list[guild_id][index_s]
                    if index_name.startswith('http'):
                        next_info = get_video_info1(url=index_name)
                        if next_info==None:
                            next_info = get_video_info(url=index_name)
                        next_video_title = next_info['title']
                    else:
                        next_video_title = index_name
                if self.repeat[str(guild_id)] == '반복재생':
                    current_index = self.playlists[guild_id].index(self.current_song[guild_id])
                    # index=current_index
                    current_index = self.playlists[guild_id][current_index]
                    if current_index.startswith('http'):
                        next_info = get_video_info1(url=current_index)
                        if next_info==None:
                            next_info = get_video_info(url=current_index)
                        next_video_title = next_info['title']
                    else:
                        next_video_title = current_index
                if self.repeat[str(guild_id)] == '일반재생':
                    next_video_title = '현재곡 재생후 정지'
                time_formatted = self.convert_seconds_to_time_format(seconds=d_time)
                embed=discord.Embed(title='타이틀', description=video_title, color=0xFF5733)
                embed.set_author(name=state, url="https://example.com", icon_url="https://i.imgur.com/Eze649t.gif")
                embed.set_thumbnail(url=thumbnail_url)
                embed.add_field(name="노래길이", value=time_formatted, inline=True)
                embed.add_field(name="재생목록", value=f'{file_name}의{len(self.playlists[guild_id])}개음악', inline=True)
                embed.add_field(name="볼륨", value=f'{(self.volume[guild_id]*100)}%', inline=True)
                embed.add_field(name="재생모드", value=self.repeat[str(guild_id)])
                embed.add_field(name="다음곡", value=next_video_title, inline=True)
                embed.add_field(name="조작자", value=name, inline=True)
                embed.set_footer(text="짭냥이플레이어 V 0.30", icon_url="https://i.imgur.com/VlKtyVf.png")
                return embed
        except Exception as e:
            traceback.print_exc()
            print(e)
    async def set_volume(self, ctx, volume: float):
        guild_id=str(ctx.guild.id)
        if ctx.voice_client is None:
            return await ctx.send("봇이 음성 채널에 들어가지 않았습니다.")

        if 0 > volume > 100:
            return await ctx.send("음량을 0과 100 사이의 값으로 입력해주세요.")
        if guild_id not in self.volume:
            self.volume[str(ctx.guild.id)]=0.5

        self.volume[str(ctx.guild.id)] = volume / 100
        if ctx.voice_client.is_playing():
            ctx.voice_client.source.volume = self.volume[str(ctx.guild.id)]
        if str(ctx.guild.id) in self.channel_id:
            await self.music(ctx,rest=True)

        await ctx.send(f"볼륨이 {self.volume[str(ctx.guild.id)]*100}%로 조정되었습니다.\n과한 볼륨상승시 음질손상이 있습니다. 적당하게 올려주세요", delete_after=2)
    async def music(self, ctx,rest=False,inuser_id=None):
            client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
            db = client['music']
            try:
                guild_id=str(ctx.author.guild.id)
                guild_name=str((ctx.author.guild.name))
                if guild_id not in self.file:
                    self.file[guild_id]='없음'
                if inuser_id is None:
                    user_id=str(ctx.author.id)
                    if ctx.author.global_name is None:
                        user_name=str(ctx.author.name)
                    else:
                        user_name=str(ctx.author.global_name)
                else:
                    user_id=int(inuser_id)
                    user=self.bot.get_user(user_id)
                    if user.global_name is None:
                        user_name=str(user.name)
                    else:
                        user_name=str(user.global_name)
                folder_path = f'./sound/{guild_id}'
                if guild_id not in self.volume:
                    self.volume[str(ctx.guild.id)]=0.5
                if guild_id not in self.repeat:
                    self.repeat[str(guild_id)] = '일반재생'
                if guild_id not in self.playing:
                    self.playing[str(guild_id)] = '정지'
                if rest==False:
                    try:
                        if guild_id in self.msg:
                            channel = self.bot.get_channel(int(self.channel_id[guild_id][0]))
                            message = await channel.fetch_message(int(self.msg[guild_id][0]))
                            await message.delete()
                    except Exception as e:
                        print(e)
                        self.playlists[guild_id]=[]
                        self.options[guild_id]=[]
                        # if not guild_id in self.current_song[guild_id]:
                        self.current_song[guild_id]=None
                        self.components[guild_id]=[]
                    else:
                        self.playlists[guild_id]=[]
                        self.options[guild_id]=[]
                        # if not guild_id in self.current_song[guild_id]:
                        self.current_song[guild_id]=None
                        self.components[guild_id]=[]
                if len(self.playlists[guild_id])>0:
                    self.options[guild_id]=[]
                    seen_urls = set()

                    for index, url in enumerate(self.playlists[guild_id], start=1):
                        if url in seen_urls:
                            continue
                        if len(seen_urls) == 25:  # 플레이리스트에 25개의 노래가 이미 있다면
                            await ctx.send("플레이 리스트 25개 이상은 아직 추가할수 없습니다.", delete_after=2)
                            break
                        seen_urls.add(url)
                        # if "list" in url:  # Check if "list" exists in the URL
                        #     continue
                        if url.startswith('http'):
                            info = get_video_info1(url=url)
                            video_title = info.get('title')
                            if video_title is None:
                                await ctx.send(f'{url}의 정보를 불러올수 없습니다.')
                                return
                            numbered_video_title = f"{index}. {video_title}"
                            if len(numbered_video_title) > 100:
                                numbered_video_title = numbered_video_title[:100]
                            self.options[guild_id].append(discord.SelectOption(label=numbered_video_title, value=url))
                    
                        elif not url.startswith('http'):
                            path = os.path.join(folder_path, url)
                            numbered_label = f"{index}. {url}"
                            if len(numbered_label) > 100:
                                numbered_label = numbered_label[:100]
                            self.options[guild_id].append(discord.SelectOption(label=numbered_label, value=url))
                        else:
                            await ctx.send(f'{url}은 리스트 추가가능한 형식이 아닙니다.\n 해당곡은 제외되서 출력됩니다! ', delete_after=2)

                elif len(self.playlists[guild_id])==0 and rest==False:
                    self.options[guild_id].append(discord.SelectOption(label="목록이 없습니다.", value="0"))
                if self.current_song[guild_id] is not None:
                    if self.current_song[guild_id].startswith('http'):
                        info = get_video_info1(url=self.current_song[guild_id])
                        title = info['title']
                        place_name=f'재생중▶️{title}'
                    else:
                        title = self.current_song[guild_id]
                        place_name=f'재생중▶️{self.current_song[guild_id]}'
                else:
                    place_name='곡을 선택해 주세요'
                self.components[guild_name] = [
                    discord.ui.Button(style=discord.ButtonStyle.primary, emoji="⏯️", custom_id=f'{guild_id}Play/Pause'),
                    discord.ui.Button(style=discord.ButtonStyle.primary, emoji="⏹️", custom_id=f'{guild_id}Stop'),
                    discord.ui.Button(style=discord.ButtonStyle.primary, emoji="⏭️", custom_id=f'{guild_id}Next'),
                    discord.ui.Button(style=discord.ButtonStyle.primary, emoji="🔁", custom_id=f'{guild_id}Repeat'),
                    discord.ui.Button(style=discord.ButtonStyle.primary, emoji="🔀", custom_id=f'{guild_id}Shuffle'),
                    discord.ui.Select(custom_id=f'{guild_id}select', placeholder=place_name, options=self.options[guild_id],min_values=0),
                    discord.ui.Button(style=discord.ButtonStyle.primary, label='폴더',emoji="📁", custom_id=f'{guild_id}개인'),
                    discord.ui.Button(style=discord.ButtonStyle.primary,label='서버', emoji="📁", custom_id=f'{guild_id}서버유'),
                    discord.ui.Button(style=discord.ButtonStyle.primary, label='개인',emoji="📁", custom_id=f'{guild_id}개인유'),
                    discord.ui.Button(style=discord.ButtonStyle.red, emoji="❌", custom_id=f'{guild_id}disconnect')
                ]
                # if os.path.isdir(folder_path):
                #     self.components[guild_name].append(discord.ui.Button(style=discord.ButtonStyle.primary, label='폴더',emoji="📁", custom_id=f'{guild_id}개인'))
                # if guild_id in db.list_collection_names():
                #     self.components[guild_name].append(discord.ui.Button(style=discord.ButtonStyle.primary,label='서버', emoji="📁", custom_id=f'{guild_id}서버유'))
                # if user_id in db.list_collection_names():
                #     self.components[guild_name].append(discord.ui.Button(style=discord.ButtonStyle.primary, label='개인',emoji="📁", custom_id=f'{guild_id}개인유'))

                # self.components[guild_id].append(components)
                view = View(timeout=None)
                for value in self.components[guild_name]:
                    if isinstance(value, discord.ui.Select):
                        value.callback = self.select_callback
                    else:
                        value.callback = self.on_button_click
                    view.add_item(value)

                embed= self.embed(title=None,file_path=folder_path,guild_id=guild_id,name=user_name)

                if rest is False:
                    msg = await ctx.send(embed=embed, view=view)
                    self.msg[guild_id] = [str(msg.id)]
                    self.channel_id[guild_id]=[]
                    self.channel_id[guild_id].append(f'{ctx.channel.id}')
                    return
                elif rest is True:
                    channel = self.bot.get_channel(int(self.channel_id[guild_id][0]))
                    message = await channel.fetch_message(int(self.msg[guild_id][0]))
                    await message.edit(embed=embed, view=view)
                    return
            except Exception as e:
                if "components.1.components.0.options" in str(e):
                    await ctx.send('재생목록은 25개를 넘어설수 없습니다! 25개 이하로 삭제해 주세요!',delete_after=2)
                print(e)
                traceback.print_exc()
                if "The specified option value is already used" in str(e):
                    # self.playlists[guild_id]=[]
                    # self.options[guild_id]=[]
                    # self.current_song[guild_id]=None
                    # self.components[guild_id]=[]
                    # await self.music(ctx,rest=False)
                    print(e)
        
    async def add_u_link(self,ctx,index=None,url=None):
        # Only respond to commands from users with the correct permissions
        if ctx.author.guild_permissions.administrator:
            # if not url.startswith('https://www.youtube.com/watch?v='):
            #     await ctx.channel.send(f'허용되는 주소가 아닙니다.\n``https://www.youtube.com/watch?v=``형식으로 시작되는 주소로 넣어주세요!', delete_after=5)
            #     return
            guild_id = str(index)
            client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
            db = client['music']
            collection = db[guild_id]
            video_info = get_video_info(url)
            info=video_info['title']
            video_id=extract_video_id(url=url)
            new_url=f"https://www.youtube.com/watch?v={video_id}"
            # db = client['mydatabase']
            # collection = db['channels']
            # Check if the channel ID is already in the collection
            existing_channel = collection.find_one({'url': new_url})
            if video_info is None:
                await ctx.channel.send(f'주소가 정확하지 않습니다.', delete_after=5)
                return
            if existing_channel:
                await ctx.channel.send(f'{info}은 이미 추가되어 있습니다.', delete_after=5)
                return
            else:
                # Insert a new document in the collection
                collection.insert_one({'name': info, 'url': new_url, 'info': info})
                await ctx.channel.send(f'{info}이(가) 유튜브 목록에 추가됨!', delete_after=2)
                return
        else:
            await ctx.channel.send('권한이 없습니다', delete_after=0.5)
            return
    @commands.hybrid_command ( name = '검색', with_app_command = True,description="유튜브에서 음악을 검색함")
    @commands.guild_only()
    async def with_app_command1231222333(self, ctx: commands.Context,*,keyword):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.찾기(ctx,keyword=keyword)
    @commands.hybrid_command ( name = '귀여워', with_app_command = True,description="짭냥이플레이어를 실행합니다." )
    @commands.guild_only()
    async def with_app_command123123(self, ctx: commands.Context):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.music(ctx,rest=False)
        # await ctx.send('현재 서버오류로 수정중에 있음.')
    @commands.hybrid_command ( name = '볼륨', with_app_command = True,description="봇의 음량을 조정합니다(1~99)값입력" )
    @commands.guild_only()
    async def 볼륨_with_app_command(self, ctx: commands.Context,volume: int):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.set_volume(ctx, volume)
            
    @commands.hybrid_command ( name = '개리업', with_app_command = True,description="개인유트브 음악목록을 표기함")
    async def with_app_command(self, ctx: commands.Context):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
                await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        index=ctx.author.id
        await self.목록(ctx,index=index,title='개인')
    @commands.hybrid_command ( name = '서리업', with_app_command = True,description="서버유트브 음악목록을 표기함")
    @commands.guild_only()
    async def with_app_command1(self, ctx: commands.Context):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
                await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        index=ctx.guild.id
        await self.목록(ctx,index=index,title='서버')
    @commands.hybrid_command ( name = '개인저장', with_app_command = True,description="!유트브 링크로 개인리스트에 저장합니다." )
    @commands.guild_only()
    async def slash_with_app_command122(self, ctx: commands.Context,url:str):
        m_name=ctx.author.id
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.add_u_link(ctx,index=m_name,url=url)
    @commands.hybrid_command ( name = '서버저장', with_app_command = True,description="!유트브 링크로 서버리스트에 저장합니다." )
    @commands.guild_only()
    async def slash_with_app_command1111(self, ctx: commands.Context,url:str):
        m_name=ctx.guild.id
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.add_u_link(ctx,index=m_name,url=url)
async def setup(bot):
    await bot.add_cog(MusicControl(bot))