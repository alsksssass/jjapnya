import discord
from discord.ext import commands
import pymongo

class SetPassword(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mongo_client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.mongo_client['plog']

    async def save_data(self, ctx, guild_id, channel_id, password, content):
        collection = self.db[str(guild_id)]
        collection.insert_one({'channel_id': channel_id, 'password': password, 'content': content})
        await ctx.send(f'비번 {password}에 {content} 내용이 {ctx.channel.name}에 기록됨!', delete_after=2)

    async def get_matching_content(self,ctx,guild_id, password):
        collection = self.db[str(guild_id)]
        cursor = collection.find({'password': password})
        matching_content = [{'channel_id': doc['channel_id'], 'content': doc['content']} for doc in cursor]
        return matching_content


    async def delete_matching_content(self,ctx, guild_id, password):
        collection = self.db[str(guild_id)]
        result = collection.delete_many({'password': password})
        return result.deleted_count
    
    async def list_passwords(self, ctx: commands.Context,guild_id):
        """
        Lists all the passwords that have been used to log messages on the server
        """
        collection_name = str(guild_id) # Set the collection name to "222"
        collection = self.db[collection_name]
        cursor = collection.find({})
        password_counts = {}

        for doc in cursor:
            password = doc['password']
            channel_id = doc['channel_id']
            channel = self.bot.get_channel(int(channel_id))
            if not channel:
                continue
            try:
                channel_name = channel.name
            except AttributeError:
                channel_name = 'Unknown'

            if password in password_counts:
                password_counts[password]['count'] += 1
                password_counts[password]['channels'].add(channel_name)
            else:
                password_counts[password] = {'count': 1, 'channels': {channel_name}}

        if password_counts:
            password_list = '\n'.join([f"비밀번호: {password}로 저장된 로그: {count}개, 출력 채널: {', '.join(channels)}" for password, data in password_counts.items() for count in [data['count']] for channels in [data['channels']]])
            await ctx.send(f"저장된 비밀번호 목록:\n{password_list}")
        else:
            await ctx.send("저장된 비밀번호가 없습니다.")




    # @commands.command(name='비번기록')
    # @commands.has_permissions(administrator=True)
    # async def prefix(self, ctx: commands.Context, password: str, *content):
    #         channel_id = str(ctx.channel.id)
    #         content = ' '.join(content)
    #         await self.save_data(ctx,ctx.guild.id, channel_id, password, content)
    #         await ctx.channel.send(f'비번 {password}에 {content} 내용이 {ctx.channel.name}에 기록됨!', delete_after=2)

        
    @commands.hybrid_command(name='비번기록', with_app_command=True, description="채널에 !비번으로 출력될 내용을 기록합니다.")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def slash_with_app_command(self, ctx: commands.Context, password: str, *,content: str):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.save_data(ctx,ctx.guild.id, str(ctx.channel.id), password, content)
        # await ctx.send(f'비번 {password}에 {content} 내용이 {ctx.channel.name}에 기록됨!', delete_after=2)

    # @commands.command(name='비번')
    # async def check_password(self, ctx: commands.Context, password: str):
    #     matching_content = await self.get_matching_content(ctx,ctx.guild.id, password)
    #     if matching_content:
    #         await ctx.send(f"{ctx.author.nick}님이 {password}을/를 풀어냈습니다.")
    #         for content in matching_content:
    #             channel_id = content['channel_id']
    #             channel = self.bot.get_channel(int(channel_id))
                
    #             await channel.send(content['content'])
    #     else:
    #         await ctx.send(f'{password} 🚫 일치하는 내용이 없습니다.')
    
    @commands.hybrid_command(name='비번', with_app_command=True, description="!비번으로 저장된 내용을 출력합니다.(모두사용가능)")
    @commands.guild_only()
    async def slash1_with_app_command(self, ctx: commands.Context, 비번:str):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        nick_name=ctx.author.nick or ctx.author.global_name or ctx.author.name
        await ctx.send(content=f"{nick_name}님이 {비번}으로 확인중...")
        matching_content = await self.get_matching_content(ctx,ctx.guild.id, 비번)
        if matching_content:
            await ctx.send(f"{ctx.author.nick}님이 {비번}을/를 풀어냈습니다.")
            for content in matching_content:
                channel_id = content['channel_id']
                channel = self.bot.get_channel(int(channel_id))
                if content['content'] is None:
                    content='없음'
                else:
                    content=content['content']
                await channel.send(content)
        else:
            await ctx.send(f'{비번} 🚫 일치하는 내용이 없습니다.')

    # @commands.command(name='비번삭제')
    # @commands.has_permissions(administrator=True)
    # async def delete_matching_content_prx (self, ctx: commands.Context, password: str):
    #     deleted_count = await self.delete_matching_content(ctx,ctx.guild.id, password)
    #     await ctx.send(f'비번 {password}와 일치하는 {deleted_count}개의 로그가 삭제되었습니다.')
    
    @commands.hybrid_command(name='비번삭제', with_app_command=True, description="!비번 으로 기록된 내용을 삭제합니다.")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def slash2_with_app_command(self, ctx: commands.Context, 비번:str):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        deleted_count = await self.delete_matching_content(ctx,ctx.guild.id, 비번)
        await ctx.send(f'비번 {비번}와 일치하는 {deleted_count}개의 로그가 삭제되었습니다.')
        
    # @commands.command(name='비번목록')
    # async def list_passwords_prx(self, ctx: commands.Context):
    #     await self.list_passwords(ctx,ctx.guild.id)
    
            
    @commands.hybrid_command(name='비번목록', with_app_command=True, description="저장된 비번리스트를 불러옵니다.")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def slash3_with_app_command(self, ctx: commands.Context):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.list_passwords(ctx,ctx.guild.id)

    
async def setup(bot):
    await bot.add_cog(SetPassword(bot))
