import discord
from discord.ext import commands, tasks
import socket
import random
import string
import pymongo
from bson import ObjectId
from collections import Counter
import asyncio
from asyncio import sleep
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
# import logging

# logging.basicConfig(level=logging.DEBUG)
def format_member_name(member):
    if member.global_name and not member.global_name[0].isdigit():
        return member.global_name
    elif not member.name[0].isdigit():
        return member.name
    else:
        return str(member.id)

class Admin_option(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def module(self,ctx):
        await ctx.channel.send('ping')
    async def create_invite(self,channel):
        if channel.permissions_for(channel.guild.me).create_instant_invite:
            return await channel.create_invite()
        return None
    @commands.command()
    async def 길드정보(self, ctx):
        if ctx.author.id == 317655426868969482:
            guild_list = []
            
            for guild in self.bot.guilds:
                guild_info = f'[{guild.owner.global_name}ㅣ{guild.owner.name}] \n[{guild.owner.id}]\n[{guild.name}]\n[{guild.id}]\n---\n'
                
                # Check if adding the guild_info exceeds the character limit
                if len('\n'.join(guild_list)) + len(guild_info) > 1500:
                    # Send the current guild_list and reset it
                    await ctx.channel.send(''.join(guild_list))
                    guild_list = []
                
                guild_list.append(guild_info)
            
            # Send the remaining guild_list if it's not empty
            if guild_list:
                await ctx.channel.send(''.join(guild_list))
            
            count = len(self.bot.guilds)
            await ctx.channel.send(f'{count}개 길드 확인됨')
        guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
        channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
        await channel.send(f'{ctx.author.name}님이{ctx.guild.name}에서 ㅇㅇㅇ명령어 사용')
    
    @commands.command()
    async def 길드제외(self,ctx, *, guildinput:int):  
        if ctx.author.id == 317655426868969482:
            
            guildid = int(guildinput)   
            
            guild = self.bot.get_guild(guildid)         
            await guild.leave()             
            await ctx.send(f"left {guild.name}")         
    
    @commands.command()
    async def 아이피(self,ctx):
        if ctx.author.id == 317655426868969482:
            # Get the hostname of the server
            hostname = socket.gethostname()

            # Get the IP address of the server
            ip_address = socket.gethostbyname(hostname)

            await ctx.channel.send(f'Server hostname:, {hostname}')
            await ctx.channel.send(f'Server IP address:, {ip_address}')
    
    @commands.command()
    async def 타임초기화(self,ctx):
        if ctx.author.id == 317655426868969482:
            self.bot.timer_runing == False
            await ctx.channel.send(f'{self.bot.timer_runing}')
    
    @commands.command()
    async def 디엠(self,ctx, user_id: int, *, message: str):
        if ctx.author.id == 317655426868969482:
            user = self.bot.get_user(user_id)
            if user is not None:
                await user.send(message)
                await ctx.send(f'{user_id}에게 전송됨')
            else:
                await ctx.send(f"Could not find a user with the ID {user_id}")
    
    @commands.command()
    async def 핑(self, ctx):
        await ctx.send(f'{self.bot.user.display_name}')
        await ctx.send(f'{ctx.author.display_name}')
        await ctx.send(f'{ctx.author.global_name}')
        all_user_ids = []
        
        for guild in self.bot.guilds:
            # Get a list of all user IDs in the guild, excluding the guild owner's ID
            user_ids = [member.id for member in guild.members if member.id != guild.owner_id and member.id != self.bot.user.id]
            all_user_ids.extend(user_ids)
        
        # Count the occurrences of each user ID
        user_counts = Counter(all_user_ids)
        
        # Get the top 3 most common user IDs
        top_3 = user_counts.most_common(3)
        
        # Check for ties and include them in the top 3
        tied_users = [user for user, count in user_counts.items() if count == top_3[-1][1] and user not in [x[0] for x in top_3]]
        top_3.extend([(user, top_3[-1][1]) for user in tied_users])
        
        # Print the results
        print("최다 플레이어:")
        for i, (user_id, count) in enumerate(top_3):
            # Get the global name of the user
            user = await self.bot.fetch_user(user_id)
            global_name = f"{user.global_name}"
            
            print(f"{i+1}위.{global_name}, {count}회")
    
    @commands.hybrid_command ( name = '진행랭킹', with_app_command = True,description="탑10 진행자 목록을 불러옵니다." )
    async def 진행랭킹(self, ctx):
        client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
        db = client['list_out']
        collection = db['list'] # Replace with your collection name

        # Get the list of guild IDs from MongoDB
        subscribed_guild_ids = [doc['guild_id'] for doc in collection.find()]
        user_ids = []
        for guild in self.bot.guilds:
            # Only consider non-subscribed guilds
            if guild.id not in subscribed_guild_ids:
                # Send message to the guild owner
                user_ids.append(guild.owner.id)

        counts = Counter(user_ids)
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)

        result = []
        top_counts = [sorted_counts[i][1] for i in range(10)]
        list_rank = []
        previous_count = 0  # Initialize the variable here
        current_rank = 0  # Initialize the variable here
                    
        for value, count in sorted_counts:
            if count in top_counts:
                result.append((value, count))
        list_rank.append('진행 랭킹 탑10 :\n')
        for value, count in result:

            current_rank += 1


            b_name = self.bot.get_user(value)
            if b_name.global_name is None:
                nick_b = b_name.name
            else:
                nick_b = b_name.global_name
            str_r = f'{current_rank}위 {nick_b}님 {count}건\n'
            list_rank.append(str_r)

        await ctx.author.send(''.join(list_rank))
        await ctx.send(f'해당 기록이 디엠으로 전송되었습니다.', delete_after=1)
    

    @commands.hybrid_command ( name = '플레이랭킹', with_app_command = True,description="탑10 플레이어를 불러옵니다." )
    async def 플레이랭킹(self, ctx):
        client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
        db = client['list_out']
        collection = db['list'] # Replace with your collection name

        # Get the list of guild IDs from MongoDB
        subscribed_guild_ids = [doc['guild_id'] for doc in collection.find()]
        # Get a list of all user IDs in all guilds, excluding the guild owner's and bot's IDs
        all_user_ids = [member.id for guild in self.bot.guilds for member in guild.members if member.id != guild.owner_id and member.id != self.bot.user.id and guild.id not in subscribed_guild_ids]
        
        # Count the occurrences of each user ID
        user_counts = Counter(all_user_ids)
        
        # Get the top 100 most common user IDs
        top_100 = user_counts.most_common(10)
        
        # Check for ties and include them in the top 100
        tied_users = [user for user, count in user_counts.items() if count == top_100[-1][1] and user not in [x[0] for x in top_100]]
        top_100.extend([(user, top_100[-1][1]) for user in tied_users])
        
        # Print the results
        list_play_rank = [f"최다플레이 랭크 탑10:\n"]
        for i, (user_id, count) in enumerate(top_100):
            # Get the global name of the user
            user = await self.bot.fetch_user(user_id)
            global_name = user.global_name or user.name
            
            list_play_rank.append(f"{i+1}위.{global_name}, {count}회플레이\n")
        await ctx.author.send(''.join(list_play_rank))
        await ctx.send(f'해당 기록이 디엠으로 전송되었습니다.', delete_after=1)
    @commands.hybrid_command ( name = '플레이기록',aliases=['한거'], with_app_command = True,description="본인이 플레이한 크씬목록을 불러옵니다." )
    async def 플레이기록(self,ctx):
        client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
        db = client['list_out']
        collection = db['list'] # Replace with your collection name

        # Get the list of guild IDs from MongoDB
        subscribed_guild_ids = [doc['guild_id'] for doc in collection.find()]
        play_list=['짭냥이가 있는곳만 표시됨:\n날짜순 정렬\n']
        member_id = ctx.author.id  # 명령어를 입력한 사용자의 id
        guilds = self.bot.guilds  # 봇이 참여하고 있는 모든 길드

        # 해당 id의 사용자가 참가하고 있는 모든 길드 찾기
        member_guilds = [guild for guild in guilds if guild.get_member(member_id) is not None and guild.owner_id != member_id and guild.id not in subscribed_guild_ids]
        member_guilds.sort(key=lambda x: x.get_member(member_id).joined_at, reverse=True)
        play_list.append(f"총 {len(member_guilds)}개 \n")
        # 찾은 길드의 이름을 출력
        for i, guild in enumerate(member_guilds):
            user_join_date = guild.get_member(member_id).joined_at.strftime("%Y-%m-%d %H:%M:%S")
            if guild.owner and guild.owner.global_name:
                owner_name = guild.owner.global_name
            else:
                owner_name = guild.owner.name
            play_list.append(f"--\n{i+1}\n {guild.name}  \n 진행자{owner_name}\n   최초 접속 날짜: {user_join_date}\n")
            if len(''.join(play_list)) > 1500:
                # Send the current guild_list and reset it
                await ctx.author.send(''.join(play_list))
                play_list = []
        if play_list:
            await ctx.author.send(''.join(play_list))
        await ctx.send(f'해당 기록이 디엠으로 전송되었습니다.', delete_after=1)
    @commands.hybrid_command(name='안한기록', aliases=['안한거'], with_app_command=True, description="본인이 플레이하지 않은 크씬목록을 불러옵니다.")
    async def 안한플레이기록(self, ctx):
        client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
        db = client['list_out']
        collection = db['list']  # Replace with your collection name

        # Get the list of guild IDs from MongoDB
        subscribed_guild_ids = [doc['guild_id'] for doc in collection.find()]
        play_list = ['짭냥이가 있는 곳만 표시됨(진행한 크씬 제외):\n서버 개설일순 정렬\n']
        member_id = ctx.author.id  # 명령어를 입력한 사용자의 id
        guilds = self.bot.guilds  # 봇이 참여하고 있는 모든 길드

        # 해당 id의 사용자가 참가하지 않은 모든 길드 찾기
        member_guilds = [guild for guild in guilds if guild.get_member(member_id) is None and guild.id not in subscribed_guild_ids]
        
        # 길드 창설일 기준 최신순 정렬
        member_guilds.sort(key=lambda x: x.created_at, reverse=True)

        play_list.append(f"총 {len(member_guilds)}개 \n")

        # 찾은 길드의 이름을 출력
        for i, guild in enumerate(member_guilds):
            if guild.owner and guild.owner.global_name:
                owner_name = guild.owner.global_name
            else:
                owner_name = guild.owner.name
            guild_creation_date = guild.created_at.strftime("%Y-%m-%d %H:%M:%S")
            play_list.append(f"--\n{i+1}\n {guild.name}  \n 진행자 {owner_name},\n   창설 날짜: {guild_creation_date}\n")
            if len(''.join(play_list)) > 1500:
                # Send the current guild_list and reset it
                await ctx.author.send(''.join(play_list))
                play_list = []
        if play_list:
            await ctx.author.send(''.join(play_list))
        await ctx.send(f'해당 기록이 디엠으로 전송되었습니다.', delete_after=1)

        
    @commands.hybrid_command ( name = '플레이비교', aliases=['비교'], with_app_command = True,description="@로 선택한 다른 플레이어와 기록을 비교합니다." )
    @commands.guild_only()
    async def play_check(self, ctx, targets: commands.Greedy[discord.Member]):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send('경고: 이 명령어는 서버에서만 사용 가능합니다.dm에서 불가!')
            return
        client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
        db = client['list_out']
        collection = db['list'] # Replace with your collection name

        # Get the list of guild IDs from MongoDB
        subscribed_guild_ids = [doc['guild_id'] for doc in collection.find()]

        # 모든 길드에 대해 각 타겟이 참가하고 있는지 확인
        excluded_guilds = []
        for guild in self.bot.guilds:
            if all(guild.get_member(target.id) is None for target in targets) and guild.id not in subscribed_guild_ids:
                excluded_guilds.append(guild)

        # 타겟 사용자가 모두 참가하지 않은 길드가 없는 경우
        if not excluded_guilds:
            await ctx.send("모든 사용자가 참가하지 않은 크씬이 없습니다.")
            return

        # 타겟 사용자가 모두 참가하지 않은 길드가 있는 경우
        response = [f"모두 하지않은 크씬 {len(excluded_guilds)}개:\n"]
        for i, guild in enumerate(excluded_guilds):
            guild_name = guild.name
            if guild.owner and guild.owner.global_name:
                owner_name = guild.owner.global_name
            else:
                owner_name = guild.owner.name
            guild_creation_date = guild.created_at.strftime("%Y-%m-%d %H:%M:%S")
            formatted_line = f"--\n{i+1}\n [{guild.name}]\n  진행자: [{owner_name}]\n   창설날짜:[{guild_creation_date}]\n    플레이한 숫자: [{guild.member_count}]\n"
            response.append(formatted_line)
            if len(''.join(response)) > 1500:
                # Send the current guild_list and reset it
                await ctx.author.send(''.join(response))
                response = []

        formatted_response = "\n".join(response)

        if formatted_response:
            await ctx.author.send(''.join(formatted_response))
        await ctx.send(f'해당 기록이 디엠으로 전송되었습니다.', delete_after=1)

    @commands.hybrid_command ( name = '한사람', with_app_command = True,description="서버아이디로 플레이한 인원목록을 불러옵니다." )
    async def list_users(self, ctx, guild_id: int):
        guild = discord.utils.get(self.bot.guilds, id=guild_id)

        if not guild:
            await ctx.send("해당 서버를 찾을 수 없습니다. 올바른 길드 ID를 입력해 주세요.")
            return

        # 서버의 모든 멤버 출력
        members = [format_member_name(member) for member in guild.members]
        response = [f"{guild.name} 총 플레이어 {len(members)}명:\n"]
        response.append("\n".join(members))
        
        response_str = "".join(response)
        if len(response_str) > 1500:
            parts = [response_str[i:i + 1500] for i in range(0, len(response_str), 1500)]
            for part in parts:
                await ctx.author.send(part)
        else:
            await ctx.author.send(response_str)
        await ctx.send(f'{guild.name}관련 기록이 디엠으로 전송되었습니다.', delete_after=1)

    @commands.hybrid_command ( name = '크씬목록', with_app_command = True,description="짭냥이가 있는 크씬목록을 불러옵니다." )
    async def 크씬목록(self, ctx):
        async def send_message(ctx, message):
            chunks = [message[i:i + 1500] for i in range(0, len(message), 1500)]
            for chunk in chunks:
                await ctx.author.send(chunk)

        client = pymongo.MongoClient(
            "mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
        db = client['list_out']
        collection = db['list']  # Replace with your collection name

        # Get the list of guild IDs from MongoDB
        subscribed_guild_ids = [doc['guild_id'] for doc in collection.find()]
        play_list = ['짭냥이가 있는곳만 표시됨(개발중크씬,4인이하 제외):\n']
        guilds = self.bot.guilds  # 봇이 참여하고 있는 모든 길드

        # 봇이 참여하고 있으며 subscribed_guild_ids에 포함되지 않은 모든 길드 찾기
        all_guilds_excluding_subscribed = [guild for guild in guilds if guild.id not in subscribed_guild_ids]

        # 정렬: guild.member_count가 높은 순으로 정렬
        all_guilds_excluding_subscribed.sort(key=lambda guild: guild.member_count, reverse=True)
        real_result=0
        play_list.append(f"총 {len(all_guilds_excluding_subscribed)}개 \n")
        for i, guild in enumerate(all_guilds_excluding_subscribed):
            if guild.member_count > 4:
                if guild.owner and guild.owner.global_name:
                    owner_name = guild.owner.global_name
                else:
                    owner_name = guild.owner.name
                guild_creation_date = guild.created_at.strftime("%Y-%m-%d %H:%M:%S")
                play_list.append(
                    f"--\n{i+1}. [{guild.name}]\n   진행자: [{owner_name}]\n   길드ID: [{guild.id}]\n   창설날짜:[{guild_creation_date}]\n    플레이한 숫자: [{guild.member_count}]\n"
                )
                real_result+=1
        play_list.append(
                    f'{len(all_guilds_excluding_subscribed)}개중 5인이상{real_result}개 출력완료')
        message = ''.join(play_list)
        await send_message(ctx, message)
        await ctx.send(f'해당 내용이 디엠으로 전송되었습니다.', delete_after=1)
    @commands.hybrid_command ( name = '타로마스터', with_app_command = True,description="자동화 크신 타로마스터 무료!feat.소진" )
    async def send_invite(self,ctx):
        guild_id=812915040713310250
        channel_id=1022085158960115795
        guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
        if guild is not None:
            channel = guild.get_channel(channel_id)
            if channel is not None:
                invite = await self.create_invite(channel)
                if invite is not None:
                    try:
                        await ctx.author.send(f"{guild.name} 서버의 {channel.name} 채널 초대 링크: {invite}")
                        await ctx.author.send(f"함께할 인원들을 모은뒤 같이할 날짜를 정하고 롤을 정하고 ``!롤 역할이름`` 으로 롤지 수령후 정해진 날짜에 모여서 진행하시면 됩니다.")
                        await ctx.author.send(f"DM허용 필수.")
                    except discord.errors.Forbidden:
                        await ctx.send("DM을 전송할 수 없습니다. DM 전송을 허용하도록 설정해주세요.")
                else:
                    await ctx.send("해당 채널에서 초대 링크를 생성할 수 없습니다.")
            else:
                await ctx.send("해당 서버에 지정한 ID를 가진 채널이 존재하지 않습니다.")
        else:
            await ctx.send("지정한 ID를 가진 서버를 찾을 수 없습니다.")

    # @commands.command()
    # async def 업로드(self, ctx):
    #     guild_id = str(ctx.guild.id)
    #     mongo_client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
    #     mongo_db = mongo_client["upload_id"]
    #     mongo_collection = mongo_db["id_s"]
    #     password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    #     guild_name = str(ctx.guild.name)

    #     # Check if guild_id already exists in the database
    #     if mongo_collection.count_documents({"username": guild_id}) > 0:
    #         existing_password = mongo_collection.find_one({"username": guild_id})["password"]
    #         await ctx.author.send(content=f'이미 등록됨. id : {ctx.guild.id } password: {existing_password}')
    #         return

    #     # Insert new document into the database
    #     new_user = {"username": guild_id, "password": password, "guildname": guild_name}
    #     mongo_collection.insert_one(new_user)

    #     await ctx.author.send(content=f'{guild_name}의 ID: {guild_id}\nPassword: {password}')  # Send the guild ID and password back to the user
    @commands.command(name='동의')
    async def FunctionName(self,ctx):
        if ctx.guild.id != 1134009736447148104:
            return
        member = ctx.guild.get_member(ctx.author.id)
        role = discord.utils.get(ctx.guild.roles, name='냥줍러')
        await member.add_roles(role)
        await ctx.send(f'{ctx.author.global_name},{ctx.author.name} 님이 동의 하셧습니다.')
        
    @commands.command(name='로그인')
    async def login(self, ctx):
        if str(ctx.guild.id) not in['1113460027634761728','975632483750137878']:
            return
        await ctx.send('60초안에 아이디를 입력해주세요.')

        def check_author(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            user_id = await self.bot.wait_for('message', check=check_author, timeout=60)
            await ctx.send('60초안에 비밀번호를 입력해주세요.')
            user_password = await self.bot.wait_for('message', check=check_author, timeout=60)

            if user_id.content == 'gyeongsu_0415' and user_password.content == '73카4372':
                await ctx.send('로그인 되셧습니다.')
                await ctx.send('https://cdn.discordapp.com/attachments/1117063035601813644/1117101062462111775/RPReplay_Final1686407183.mov')
            elif user_id.content == 'jiyeoni1030@kmail.com' and user_password.content == 'jiyeon_0415':
                await ctx.send('로그인 되셧습니다.')
                await ctx.send('https://i.imgur.com/rECMU90.png')
            else:
                await ctx.send('아이디 혹은 비밀번호가 잘못되었습니다.')

        except asyncio.TimeoutError:
            await ctx.send('시간이 초과되었습니다. 다시 시도해주세요.')

    def get_text_dimensions(self,text, font):
        # https://stackoverflow.com/a/46220683/9263761
        ascent, descent = font.getmetrics()

        img_width = font.getmask(text).getbbox()[2]
        img_height = font.getmask(text).getbbox()[3] + descent

        return (img_width, img_height)

    async def send_text_as_image(self, ctx, text):
        # 상대 경로를 사용하여 폰트를 불러옵니다
        font_path = "./font/NanumGothicBold.ttf"
        font = ImageFont.truetype(font_path, 20)
        # Calculate text size
        # img_width, img_height = 300, 100
        img = Image.new("RGB", (1, 1), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        img_width, img_height = self.get_text_dimensions(text=text, font=font)
        img_width += 20
        img_height += 20


        # Create a new image with the calculated size
        img = Image.new("RGB", (img_width, img_height), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        d.text((10, 10), text, fill=(0, 0, 0), font=font)

        # 이미지를 파일로 저장합니다.
        file_name = f"{ctx.guild.id}.png"
        img.save(file_name, "PNG")
        
        # 이미지를 디스코드에 전송합니다.
        try:
            await ctx.send(file=discord.File(file_name))
        except Exception as e:
            print(f"Failed to send image: {e}")
        finally:
            # 이미지 파일을 삭제합니다.
            if os.path.exists(file_name):
                os.remove(file_name)

    # 디스코드 명령에서 이 함수를 사용합니다.
    @commands.command(name="복방")
    async def non_copyable_message(self, ctx, *args):
        text = ' '.join(args)
        await self.send_text_as_image(ctx, text)







async def setup(bot):
    await bot.add_cog(Admin_option(bot)) ##길드 아이디 입력