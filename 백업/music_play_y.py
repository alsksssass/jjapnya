import discord
from discord.ui import Button, View
from discord.ext import commands
import requests
import yt_dlp
import youtube_dl
import random
import asyncio
import isodate
import pymongo
from typing import Union
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

def choose_best_audio(formats: list):
    audio_format = None
    for f in formats:
        if f['acodec'] != 'none' and (audio_format is None or f['abr'] > audio_format['abr']):
            audio_format = f
    return audio_format

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

async def list_get(self, ctx):
    guild_id = str(ctx.author.id)
    db = self.bot.mongo['music']
    collection = db[guild_id]

    music_list = []
    for music in collection.find():
        music_list.append(music)
    self.music_list=music_list


# class AddButton(discord.ui.Button):
#     def __init__(self, video_id, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.video_id = video_id

#     async def callback(self, interaction: discord.Interaction):
#         action = "추가"
#         with yt_dlp.YoutubeDL() as ydl:
#             info = ydl.extract_info(f'https://www.youtube.com/watch?v={self.video_id}', download=False)

#         video_url = info.get('webpage_url')
#         video_title = info.get('title')

#         await interaction.response.send_message(f"`{video_title}` ({video_url}) {action}되었습니다!", ephemeral=True)

# class PlayButton(discord.ui.Button):
#     def __init__(self, bot, video_id, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.video_id = video_id
#         self.bot = bot
    

            
#     async def callback(self,interaction: discord.Interaction):

#         action = "재생"
#         with yt_dlp.YoutubeDL() as ydl:
#             info = ydl.extract_info(f'https://www.youtube.com/watch?v={self.video_id}', download=False)

#         video_url = info.get('webpage_url')
#         video_title = info.get('title')

#         await interaction.response.send_message(f"`{video_title}` ({video_url}) {action}되었습니다!", ephemeral=True)


# class ButtonExtend(discord.ui.View):
#     def __init__(self, bot, video_id):
#         super().__init__(timeout=None)
#         self.add_item(AddButton(style=discord.ButtonStyle.grey, label="추가",
#                                 custom_id=f"add_{video_id}", video_id=video_id))
#         self.add_item(PlayButton(bot, style=discord.ButtonStyle.green, label="재생",
#                                  custom_id=f"play_{video_id}", video_id=video_id))
        


# class 삭제버튼(discord.ui.Button):
#     def __init__(self, index, collection, music_list, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.index = index
#         self.collection = collection
#         self.music_list = music_list

#     async def callback(self, interaction: discord.Interaction):
#         await interaction.response.send_message(f"{self.index + 1} 번 목록으로부터 항목이 삭제되었습니다!", ephemeral=True)
#         self.collection.delete_one({"name": self.music_list[self.index]["name"]})
#         # 기존 코드 삭제 작업이 필요한 경우 여기에 작성하세요.

#         # 새로운 목록을 만들고 메시지를 보냅니다.
#         self.music_list = []
#         for music in self.collection.find():
#             self.music_list.append(music)

#         for index, music in enumerate(self.music_list):
#             title = f"{index + 1}. {music['name']}"
#             embed = discord.Embed(title=title, color=0x00ff00)

#             playback_buttons = MusicCog.ButtonExtend(music['url'])
#             playback_buttons.add_item(삭제버튼(label="삭제", custom_id=f"delete_{index}", index=index, collection=self.collection, music_list=self.music_list))
#             # 다른 버튼을 추가하고 싶다면, 위와 비슷하게 여기에 추가하세요.

#             # 이전 메시지를 삭제하고 새로운 메시지를 보냅니다.
#             await interaction.message.delete()
#             await interaction.channel.send(embed=embed, view=playback_buttons)
#         # 기존 코드 삭제 작업이 필요한 경우 여기에 작성하세요.
# # # class 재생버튼(discord.ui.Button):
# # #     def __init__(self, index, music_list, *args, **kwargs):
# # #         super().__init__(*args, **kwargs)
# # #         self.index = index
# # #         self.music_list = music_list
# # #     async def callback(self, interaction: discord.Interaction):
# # #         await interaction.response.send_message(f"{self.music_list[self.index]['name']}({self.music_list[self.index]['url']})이(가) 재생되었습니다!", ephemeral=True)
# # #         await self.재생(interaction.context, self.index + 1)


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ydl_opts = {'format': 'bestaudio/best', 'noplaylist': 'True'}
        self.volume = self.bot.vol_l
        self.music_list=[]
        self.shuffle_mode=False
    class AddButton(discord.ui.Button):
        def __init__(self, bot,video_url,keyword, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.video_url = video_url
            self.keyword= keyword            
            self.bot = bot
            
        async def callback(self, interaction: discord.Interaction):
            await interaction.response.send_message('처리중입니다.',delete_after=1)
            save_name=self.keyword
            # with yt_dlp.YoutubeDL() as ydl:
            #     info = ydl.extract_info(self.video_url, download=False)

            # video_url = info.get('webpage_url')
            # video_title = info.get('title')

            if interaction.user.guild_permissions.administrator:
                guild_id = str(interaction.guild.id)
                print(interaction.guild.id)
                client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
                db = client['music']
                collection = db[guild_id]
                video_info = get_video_info(self.video_url)
                info=video_info['title']
                # db = client['mydatabase']
                # collection = db['channels']

                # Check if the channel ID is already in the collection
                existing_channel = collection.find_one({'name': save_name})
                if existing_channel:
                    await interaction.channel.send(f'{save_name}은 이미 추가된 이름입니다', delete_after=2)
                elif video_info is None:
                    await interaction.channel.send(f'주소가 정확하지 않습니다.', delete_after=2)
                else:

                    # Insert a new document in the collection
                    collection.insert_one({'name': save_name, 'url': self.video_url, 'info': info})
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
                video_info = get_video_info(self.video_url)
                info=video_info['title']
                # db = client['mydatabase']
                # collection = db['channels']

                # Check if the channel ID is already in the collection
                existing_channel = collection.find_one({'name': save_name})
                if existing_channel:
                    await interaction.channel.send(f'{save_name}은 이미 추가된 이름입니다', delete_after=2)
                elif video_info is None:
                    await interaction.channel.send(f'주소가 정확하지 않습니다.', delete_after=2)
                else:

                    # Insert a new document in the collection
                    collection.insert_one({'name': save_name, 'url': self.video_url, 'info': info})
                    await interaction.channel.send(f'{save_name}이(가) 개인유튜브 목록에 이름 추가됨!', delete_after=2)
            else:
                await interaction.channel.send('권한이 없습니다', delete_after=1)
                

    class PlayButton(discord.ui.Button):
        def __init__(self,bot, video_url, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # self.cog = cog
            self.video_url = video_url
            self.bot = bot
            self.volume = self.bot.vol_l
            
        async def callback(self, interaction: discord.Interaction):
            await interaction.response.send_message('처리중입니다.',delete_after=1)
            action = "재생"
            
            with yt_dlp.YoutubeDL() as ydl:
                info = ydl.extract_info(url=self.video_url, download=False)
            
            video_url = self.video_url
            video_title = info.get('title')
            
            user_voice_state = interaction.guild.get_member(interaction.user.id).voice
            voice_client = interaction.guild.voice_client
            if user_voice_state is None or user_voice_state.channel is None:
                return await interaction.channel.send("먼저 음성채널에 접속하셔야 합니다!",delete_after=2)
            user_voice_channel = interaction.user.voice.channel
            if not voice_client:
                voice_client = await user_voice_channel.connect()
            elif user_voice_channel != voice_client.channel:
                return await interaction.channel.send("봇이 이미 다른 음성채널에서 재생 중입니다.",delete_after=2)
            
            if voice_client.is_playing():
                voice_client.stop()

            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            with yt_dlp.YoutubeDL({'format':'bestaudio/best', 'quiet': True, 'no_warnings': True}) as ydl:
                info = ydl.extract_info(url=self.video_url, download=False)
                url_source = info['url']
                source = discord.FFmpegPCMAudio(url_source, **FFMPEG_OPTIONS)
                voice_client.play(discord.PCMVolumeTransformer(source, self.volume))


            await interaction.channel.send(f"`{video_title}` ({video_url}) {action}되었습니다!",delete_after=2)
            while voice_client.is_playing():
                await asyncio.sleep(1)
            
            await voice_client.disconnect()
            

    class ButtonExtend(discord.ui.View):
        def __init__(self, bot, video_url, keyword):
            super().__init__(timeout=None)
            self.add_item(MusicCog.AddButton(bot,style=discord.ButtonStyle.grey, label=f"'{keyword}'으/로 !음악목록 리스트에 추가",
                                    custom_id=f"add_{video_url}", video_url=video_url, keyword=keyword))
            self.add_item(MusicCog.AddButton1(bot,style=discord.ButtonStyle.grey, label=f"'{keyword}'으/로 !리스트업 리스트에 추가",
                                    custom_id=f"add_{video_url}1", video_url=video_url, keyword=keyword))
            self.add_item(MusicCog.PlayButton(bot,style=discord.ButtonStyle.green, label="재생",
                                    custom_id=f"play_{video_url}", video_url=video_url))


    # 나머지 코드는 앞과 동일합니다.
    class 삭제버튼(discord.ui.Button):
        def __init__(self, bot,ctx,index, collection, music_list, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.index = index
            self.collection = collection
            self.music_list = music_list
            self.bot=bot
            self.ctx=ctx
        async def callback(self, interaction: discord.Interaction):
            await interaction.response.send_message(f"{self.index + 1} 번  항목이 삭제되었습니다!",delete_after=2)
            self.collection.delete_one({"name": self.music_list[self.index]["name"]})
            await self.bot.get_cog('MusicCog').목록(self.ctx)


    @commands.hybrid_command ( name = '검색', with_app_command = True,description="유튜브에서 음악을 검색함")
    async def 찾기(self, ctx, *, keyword):
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

            playback_buttons = MusicCog.ButtonExtend(self.bot,video_url,keyword)
            msg = await ctx.send(embed=embed, view=playback_buttons)
            

    @commands.hybrid_command ( name = '개인추가', with_app_command = True,description="개인유트브 음악목록에 음악을 url로 추가함")
    async def 추가(self, ctx, m_name, url):
        # Only respond to commands from users with the correct permissions
        guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
        channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
        await channel.send(f'{ctx.author.name}님이{ctx.guild.name}에서 유튜브 저장 명령어 사용')
        
        guild_id = str(ctx.author.id)
        db = self.bot.mongo['music']
        collection = db[guild_id]
        video_info = self.get_video_info(url)
        info=video_info['title']
        # db = client['mydatabase']
        # collection = db['channels']

        # Check if the channel ID is already in the collection
        existing_channel = collection.find_one({'name': m_name})
        if existing_channel:
            await ctx.channel.send(f'{m_name}은 이미 추가된 이름입니다', delete_after=2)
        elif video_info is None:
            await ctx.channel.send(f'주소가 정확하지 않습니다.', delete_after=2)
        else:

            # Insert a new document in the collection
            collection.insert_one({'name': m_name, 'url': url, 'info': info})
            await ctx.channel.send(f'{m_name}이(가) 유튜브 목록에 이름 추가됨!', delete_after=2)


    @commands.hybrid_command ( name = '리스트업', with_app_command = True,description="개인유트브 음악목록을 표기함")
    async def 목록(self, ctx):
        guild_id = str(ctx.author.id)
        db = self.bot.mongo['music']
        collection = db[guild_id]
        print(self.shuffle_mode)
        async def button_callback1(interaction, ctx: commands.Context):
                if self.shuffle_mode:
                    self.shuffle_mode = False
                    await interaction.response.send_message("일반재생 모드로 변경되었습니다..", delete_after=2)
                    button_add1.label="[일반재생]모드입니다."
                    await e_msg.edit(content=f"{ctx.author.global_name}님의 개인유튜브 목록입니다.:", view=셔플_buttons)
                else:
                    self.shuffle_mode = True
                    await interaction.response.send_message("셔플재생 모드로 변경되었습니다..", delete_after=2)
                    button_add1.label="[셔플재생] 모드입니다."
                    await e_msg.edit(content=f"{ctx.author.global_name}님의 개인유튜브 목록입니다.:", view=셔플_buttons)
        async def button_callback(interaction, ctx: commands.Context):
                await interaction.response.send_message("셔플이 시작되었습니다.", delete_after=2)
                button_add1.label="[셔플재생] 모드입니다."
                await e_msg.edit(content=f"{ctx.author.global_name}님의 개인유튜브 목록입니다.:", view=셔플_buttons)
                await self.셔플(ctx)
        if self.shuffle_mode:
            mode_state='셔플재생'
        else:
            mode_state='일반재생'
        # You may also want to send a response to the interaction, like this:
        
        button_add = Button(label='셔플재생', style = discord.ButtonStyle.green, custom_id=str(ctx.author.id))
        button_add1 = Button(label=f'[{mode_state}] 모드입니다.', style = discord.ButtonStyle.green, custom_id=str(ctx.author.id*100))
        셔플_buttons = discord.ui.View(timeout=None)
        셔플_buttons.add_item(button_add)
        셔플_buttons.add_item(button_add1)
        button_add1.callback = functools.partial(button_callback1, ctx=ctx)
        button_add.callback = functools.partial(button_callback, ctx=ctx)
        # Change 'View' to 'view' in the line below
        

                                
      
        music_list = []
        
        for music in collection.find():
            music_list.append(music)
        e_msg=await ctx.send(f"{ctx.author.global_name}님의 개인유튜브 목록입니다.:", view=셔플_buttons)
        for index, music in enumerate(music_list):
            title = f"{index + 1}. {music['name']}"
            embed = discord.Embed(title=title, color=0x00ff00)
            video_url=music['url']
            keyword=music['name']
            bot=self.bot
            playback_buttons = discord.ui.View(timeout=None)
            playback_buttons.add_item(MusicCog.PlayButton(bot, style=discord.ButtonStyle.green, label="재생",
                                    custom_id=f"play_{video_url}", video_url=video_url)) 
            playback_buttons.add_item(MusicCog.삭제버튼(label="삭제", custom_id=f"delete_{index}", ctx=ctx,bot=bot,index=index, collection=collection,music_list=music_list))
            # 다른 버튼을 추가하고 싶다면, 위와 비슷하게 여기에 추가하세요.
            
            msg = await ctx.send(embed=embed, view=playback_buttons)
        self.music_list=music_list
        
        

    @commands.hybrid_command(name='재생', with_app_command=True, description="개인유트브 음악목록을 재생함 숫자,저장된이름 사용가능")
    async def 재생(self, ctx,*,index:str): 
        await list_get(self,ctx)
        
        if self.shuffle_mode is True:
            self.shuffle_mode = False
            await ctx.send("셔플모드 해제되었습니다.", delete_after=2)
        if ctx.author.voice is None:
            await ctx.send("먼저 음성 채널에 접속해주세요.", delete_after=2)
            return

        channel = ctx.author.voice.channel
        voice = ctx.guild.voice_client
        if voice is None:
            voice = await channel.connect()

        if voice.is_playing():
            voice.stop()
        
        if index.isnumeric():  # If index is a number, decrement by 1
            value = int(index)
            value -= 1
            music = self.music_list[value]
        else:  # If index is a string, find the music item with the matching name
            music = next((m for m in self.music_list if m['name'] == index), None)

        if music is None:
            await ctx.send("일치하는 음악이 없습니다.", delete_after=2)
            return

        video_url = music['url']
        video_info = get_video_info(video_url)

        if video_info is None:
            await ctx.send("유튜브 비디오 정보를 가져오는 도중 오류가 발생했습니다. 주소를 다시 확인해 주세요", delete_after=2)
            return

        audio_format = choose_best_audio(video_info['formats'])
        audio_url = audio_format['url']
        audio_title = video_info['title']

        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn',
        }

        source = discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS)
        voice.play(discord.PCMVolumeTransformer(source, self.volume))
        while voice.is_playing():
            await asyncio.sleep(1)
        if not self.bot.timer_runing:
            await voice.disconnect()


        

    @commands.hybrid_command(name='셔플', with_app_command=True, description="개인유트브 음악목록을 셔플재생함")
    async def 셔플(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("먼저 음성 채널에 접속해주세요.", delete_after=2)
            return
        self.shuffle_mode = True

        while self.shuffle_mode:
            try:
                
                await list_get(self,ctx)
                music_count = len(self.music_list)
                if music_count > 1:
                    random_index = random.randint(0, music_count - 1)
                    index = random_index + 1  # Convert index to string
                    music = self.music_list[random_index].copy()
                    m_name = music['name']
                    m_info = music['info']
                    await ctx.send(f'{index}번째곡\n{m_name}으로 저장된 \n{m_info}재생 합니다.', delete_after=2)
                    
                    
                elif music_count == 1:
                    index=1
                else:
                    await ctx.send("재생 목록에 곡이 없습니다.")
                
                
                if ctx.author.voice is None:
                    await ctx.send("먼저 음성 채널에 접속해주세요.")
                    return

                channel = ctx.author.voice.channel
                voice = ctx.guild.voice_client
                if voice is None:
                    voice = await channel.connect()

                if voice.is_playing():
                    voice.stop()
                # If index is a number, decrement by 1
                    value = int(index)
                    value -= 1
                    music = self.music_list[value]


                video_url = music['url']
                video_info = get_video_info(video_url)

                if video_info is None:
                    await ctx.send("유튜브 비디오 정보를 가져오는 도중 오류가 발생했습니다. 주소를 다시 확인해 주세요")
                    return

                audio_format = choose_best_audio(video_info['formats'])
                audio_url = audio_format['url']
                audio_title = video_info['title']

                FFMPEG_OPTIONS = {
                    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                    'options': '-vn',
                }

                source = discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS)
                voice.play(discord.PCMVolumeTransformer(source, self.volume))
                while voice.is_playing():
                    
                    if voice is None or not voice.is_connected():
                        self.shuffle_mode = False
                        await ctx.send("봇이 음성 채널에서 연결이 끊겼습니다.")
                        await ctx.send("``!멈춤``명령어 미사용시 이전음악이 플레이가끝날 시간까지 재사용 불가합니다.")
                        return
                    await asyncio.sleep(1)
            except Exception as e:
                await ctx.channel.send("재생중 오류발생")
                voice = await channel.connect()
                voice.stop()
                await voice.disconnect()
                print(e)
        await voice.disconnect()

    @commands.hybrid_command(name='재생모드', with_app_command=True, description="개인유트브 음악목록을 셔플재생함")
    async def 재생모드(self, ctx):
        if self.shuffle_mode:
            self.shuffle_mode = False
            await ctx.send("일반재생 모드입니다.")
        else:
            self.shuffle_mode = True
            await ctx.send("셔플재생 모드입니다.")

    @commands.hybrid_command ( name = '점프', with_app_command = True,description="!점프 숫자 로 개인목록의 음악을 재생함")
    async def 점프(self, ctx, index: int):
        if index < 1:
            await ctx.send("올바른 곡 순번을 입력하세요.")
            return
        await list_get(self,ctx)
        music_list_length = len(self.music_list)

        if index > music_list_length:
            await ctx.send("입력된 곡 순번이 재생 목록 범위를 벗어났습니다.")
            return
        
        
        await self.재생(ctx, index=index)


    @commands.hybrid_command ( name = '목록초기화', with_app_command = True,description="개인 유튜브 목록을 초기화함" )
    async def 목록초기화(self, ctx):
        guild_id = str(ctx.author.id)
        db = self.bot.mongo['music']
        collection = db[guild_id]

        result = collection.delete_many({})
        await ctx.send("재생 목록이 초기화되었습니다.")


            
async def setup(bot): # Add guild IDs if neededMusicCog
    await bot.add_cog(MusicCog(bot), guilds=None)