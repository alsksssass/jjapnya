import discord
from discord.ext import commands, tasks
import os
import json
import pymongo

with open('config2.json') as f:
    data = json.load(f)
    token = data["TOKEN"]
    prefix = data["prefix"]
    app_id = data["Ap_id"]
# intents = discord.Intents.all()
intents = discord.Intents.all()
# intents.message_content = True
# intents.members=True
intents.presences = False
print(intents)




# timer_running = False
global nick_name
nick_name = ""

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=prefix, intents=intents, application_id=app_id, case_insensitive=True)##어플리케이션 아이디 입력
        # self.timer_runing = False
        self.voice_client = None

    async def on_ready(self):
        await self.startup()
        # await self.load_extension("cogs.auto_disconnect")

        
    async def startup(self):
        global nick_name
        await bot.wait_until_ready()
        await bot.tree.sync(guild=None)  
        # await bot.change_presence(status=discord.Status.online, activity=discord.Game('made by 프리먼'))
        # If you want to define specific guilds, pass a discord object with id (Currently, this is global)
        print('Sucessfully synced applications commands')
        print(f'Connected as {bot.user.name}')
        

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    await bot.load_extension(f"cogs.{filename[:-3]}")

                    print(f"Loaded {filename}")
                except Exception as e:
                    print(f"Failed to load {filename}")
                    print(f"[ERROR] {e}")

        self.loop.create_task(self.startup())
    
    async def on_voice_state_update(self, member, before, after):
            if member.bot:
                self.voice_client = member.guild.voice_client
                if self.voice_client and self.voice_client.is_playing():
                    print("봇이 음성 채널에서 재생 중입니다.")
    
    async def on_command_error(self, ctx, error):
        print(error)
        try:
            if isinstance(error, commands.CommandError):
                await ctx.send(f'잘못된 명령어 입니다.\n{error}',delete_after=2)
                user_id =317655426868969482  # Replace with the specific user ID to whom you want to send the DM
                user = bot.get_user(user_id)
                server_name = ctx.guild.name if ctx.guild else 'Unknown Server'
                error_msg = f"An error occurred in server: {server_name}\nError: {error}"
                await user.send(error_msg)
        except discord.Forbidden:
            if "Cannot send messages to this user" in str(error):
                await ctx.channel.send(content="dm수신 거부 상태입니다. dm 거부시 짭냥의 기능제한이 있을수 있습니다. \n dm수락후 다시 이용해 주세요",delete_after=2)
                await user.send(error_msg)
        if "Cannot send messages to this user" in str(error):
            
            await ctx.channel.send(content="dm수신 거부 상태입니다. dm 거부시 짭냥의 기능제한이 있을수 있습니다. \n dm수락후 다시 이용해 주세요",delete_after=2)
            await user.send(error_msg)
        if isinstance(error, discord.errors.Forbidden):
            
            if "Cannot send messages to this user" in str(error):
                await ctx.channel.send(content="dm수신 거부 상태입니다. dm 거부시 짭냥의 기능제한이 있을수 있습니다. \n dm수락후 다시 이용해 주세요",delete_after=2)
                await user.send(error_msg)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send(content="명령어 뒤에 추가할 인수(숫자or문자등)이 누락되었습니다. \n다시 확인하시고 사용해 주세요",delete_after=2)
    # async def on_command_complete(self, ctx, error):
    #     user_id =317655426868969482  # Replace with the specific user ID to whom you want to send the DM
    #     user = bot.get_user(user_id)
    #     server_name = ctx.guild.name if ctx.guild else 'Unknown Server'
    #     error_msg = f"server: {server_name}\nError: {error}"
    #     await user.send(error_msg)
    async def on_message(self,message):
        target_user_id=317655426868969482
        await self.process_commands(message)
        if isinstance(message.channel, discord.DMChannel): 
            if message.author == self.user:
                return# DM 채널인지 확인
            target_user = await self.fetch_user(target_user_id)
            await target_user.send(f'이름:{message.author.name}\n아이디:{message.author.id}\n내용\n{message.content}')
        # 대상 유저에게 메시지 전송
    
        # 프로그램 로그가 생성되었을 때 실행되는 함수

        
        
bot = Bot()

bot.timer_runing = {}
bot.oriname={}
bot.guild_id=975632483750137878
bot.channel_id=1112982661753999443
bot.all_p = False
bot.player_l =[]
bot.vol_l={}
bot.mongo = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
# bot.load_extension("voice_state_cog")
bot.pre_button=[]

bot.run(token)
