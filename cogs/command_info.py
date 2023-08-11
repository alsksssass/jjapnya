import discord
from discord.ext import commands
from discord.ui import Button, View
import pymongo
class Command_info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    async def module(self,ctx):

            await ctx.author.send('```역할에서 짭냥이가 맨 위에 올라가 있어야 최고 권한권자로 여러가지 설정을 건드릴수 있습니다. 꼭 위에 올려주세요```')
            await ctx.author.send('https://i.imgur.com/XWQoaUt.png')
            max_message_length = 2000

            # Read in the file contents
            with open('./command.txt', 'r', encoding='UTF-8') as file:
                file_contents = file.read()
            async def button_callback(interaction):


                    
                    client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
                    db = client['gudock']
                    collection = db['list']
                    nick=interaction.user.id
                    # db = client['mydatabase']
                    # collection = db['channels']
                    
                    
                    # Check if the channel ID is already in the collection
                    existing_channel = collection.find_one({'user_id': nick})
                    if existing_channel:
                        
                        await interaction.response.send_message(f'{interaction.user.global_name}님은 이미 구독중입니다', delete_after=2)
                    else:
                        
                        # Insert a new document in the collection
                        collection.insert_one({'user_id': nick})
                        await interaction.response.send_message(f'{interaction.global_name}을 구독 활성화 하였습니다.', delete_after=2)
                        guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
                        channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
                        await channel.send(f'{interaction.global_name}님 구독함')

            # Break the file contents into chunks that are no larger than the maximum message length
            message_chunks = [file_contents[i:i+max_message_length] for i in range(0, len(file_contents), max_message_length)]
            buttons = discord.ui.View(timeout=None)
            end_button = Button(label="구독", style=discord.ButtonStyle.red, custom_id="종료")
            buttons.add_item(end_button)
            end_button.callback = button_callback
            # Send each message chunk as a separate message
            for chunk in message_chunks:
                await ctx.author.send(chunk)
            embed = discord.Embed(color=696969)
            
            embed.add_field(name='추가되는 기능이 생기면 아래 유튜브재생목록에 설명영상이 추가될 예정입니다.',value='https://www.youtube.com/playlist?list=PLoaEF9VgQFnWSs6Xi2otOn7j-d_J-kgmG')
            await ctx.author.send(embed=embed)
            await ctx.author.send('업데이트 되는 내용을 구독하시려면 구독 버튼을 눌러주세요\n추후``!구독``과``!구독취소``로 변경가능합니다.',view=buttons)
            guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
            channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
            await channel.send(f'{ctx.author.name}님이에서 명령어 명령어 사용')

    # async def module12(self,ctx):

    #         max_message_length = 2000

    #         # Read in the file contents
    #         with open('./usercommand.txt', 'r', encoding='UTF-8') as file:
    #             file_contents = file.read()
            
    #         # Break the file contents into chunks that are no larger than the maximum message length
    #         message_chunks = [file_contents[i:i+max_message_length] for i in range(0, len(file_contents), max_message_length)]

    #         # Send each message chunk as a separate message
    #         for chunk in message_chunks:
    #             await ctx.author.send(chunk)
            
    #         guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
    #         channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
    #         await channel.send(f'{ctx.author.name}님이에서 명령어 명령어 사용')

    
                
    @commands.hybrid_command ( name = '명령어', with_app_command = True,description="봇의 명령어 리스트를 출력합니다." )
    async def slash_with_app_command(self, ctx: commands.Context):
            if hasattr(ctx, 'interaction') and ctx.interaction is not None:
                await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
            await self.module(ctx)
    @commands.hybrid_command ( name = '유저명령어', with_app_command = True,description="유저 명령어 리스트 표출" )
    async def slash_with_app_command111(self, ctx: commands.Context):
            if hasattr(ctx, 'interaction') and ctx.interaction is not None:
                await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
            max_message_length = 2000

            # Read in the file contents
            with open('./usercommand.txt', 'r', encoding='UTF-8') as file:
                file_contents = file.read()
            
            # Break the file contents into chunks that are no larger than the maximum message length
            message_chunks = [file_contents[i:i+max_message_length] for i in range(0, len(file_contents), max_message_length)]

            # Send each message chunk as a separate message
            for chunk in message_chunks:
                await ctx.author.send(chunk)
            
            guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
            channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
            await channel.send(f'{ctx.author.name}님이에서 유저명령어 명령어 사용')
    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        owner = guild.owner
        if owner is not None:
            # 오너에게 DM 보내기
            try:
                await owner.send('```역할에서 짭냥이가 맨 위에 올라가 있어야 최고 권한권자로 여러가지 설정을 건드릴수 있습니다. 꼭 위에 올려주세요```')
                await owner.send('https://i.imgur.com/XWQoaUt.png')
                max_message_length = 2000
                add_guild=guild.name
                # Read in the file contents
                with open('./command.txt', 'r', encoding='UTF-8') as file:
                    file_contents = file.read()
                async def button_callback(interaction):

                    
                        
                        client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
                        db = client['gudock']
                        collection = db['list']
                        nick=interaction.user.id
                        # db = client['mydatabase']
                        # collection = db['channels']
                        
                        
                        # Check if the channel ID is already in the collection
                        existing_channel = collection.find_one({'user_id': nick})
                        if existing_channel:
                            
                            await interaction.response.send_message(f'{interaction.user.global_name}님은 이미 구독중입니다', delete_after=2)
                        else:
                            
                            # Insert a new document in the collection
                            collection.insert_one({'user_id': nick})
                            await interaction.response.send_message(f'{interaction.global_name}을 구독 활성화 하였습니다.', delete_after=2)
                            guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
                            channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
                            await channel.send(f'{interaction.global_name}님 구독함')

                # Break the file contents into chunks that are no larger than the maximum message length
                message_chunks = [file_contents[i:i+max_message_length] for i in range(0, len(file_contents), max_message_length)]
                buttons = discord.ui.View(timeout=None)
                end_button = Button(label="구독", style=discord.ButtonStyle.red, custom_id="종료")
                buttons.add_item(end_button)
                end_button.callback = button_callback
                # Send each message chunk as a separate message
                for chunk in message_chunks:
                    await owner.send(chunk)
                embed = discord.Embed(color=696969)
                
                embed.add_field(name='추가되는 기능이 생기면 아래 유튜브재생목록에 설명영상이 추가될 예정입니다.',value='https://www.youtube.com/playlist?list=PLoaEF9VgQFnWSs6Xi2otOn7j-d_J-kgmG')
                await owner.send(embed=embed)
                await owner.send('업데이트 되는 내용을 구독하시려면 구독 버튼을 눌러주세요\n추후``!구독``과``!구독취소``로 변경가능합니다.',view=buttons)
                guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
                channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
                await channel.send(f'길드 이름: {add_guild}, \n오너 이름: {owner.name}\n{owner.global_name}새롭게 추가됨')
            except discord.Forbidden:
                print(f"오너에게 메시지를 보낼 수 없습니다. 길드 이름: {guild.name}, 오너 이름: {owner.name}")

    
async def setup(bot):
    await bot.add_cog(Command_info(bot)) ##길드 아이디 입력