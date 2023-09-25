# import discord
# from discord import ui
# from discord.ui import Button, View
# from discord.ext import commands, tasks
# from discord.ext.commands import has_permissions, CheckFailure, HybridCommand
# import time
# import os
# import pymongo
# from datetime import datetime, timedelta
# import asyncio
# from asyncio import sleep
# import json 
# import socket
# import discord.utils
# import requests
# from pydub import AudioSegment
# import urllib.request
# import re
# from urllib.parse import urlparse
# from discord import Embed
# import openpyxl

# class Del_num_all(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot


#     # async def De_channel(self,ctx, limit:int):
#     #     if ctx.author.guild_permissions.administrator:
#     #         if limit <= 0:
#     #             await ctx.send('유효하지 않은 숫자입니다.')
#     #             return

#     #         await ctx.channel.purge(limit=limit, bulk=True)
#     #         await ctx.send(f'{limit}개의 메시지가 삭제되었습니다.', delete_after=2)
#     #         guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
#     #         channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
#     #         await channel.send(f'{ctx.author.name}님이{ctx.guild.name}에서 삭제명령어 사용')


#     async def De_channel1(self,ctx, day:int):
#         try:
#             if ctx.author.guild_permissions.administrator:
#                 guild_id = str(ctx.guild.id)
#                 client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
#                 db = client['mydatabase']
#                 collection = db[guild_id]
#                 # Get the guild ID
#                 # Read the list of channel IDs and names from the file
#                 # with open(f'{guild_id}_channels.txt', 'r') as f:
#                 documents = collection.find()
#                 current_date = ctx.message.created_at

#                 # The timedelta object represents a duration of 15 days
#                 max_age = timedelta(days=day)
#                 def check(message):
#                     message_age = current_date - message.created_at
#                     return message_age < max_age
#                 # Create a list of channel IDs and names from the documents
#                 channels_to_delete = []
#                 async def delete_old_messages(channel):
#                     messages_to_delete = []
#                     async for message in channel.history(limit=100):
#                         message_age = current_date - message.created_at
#                         if message_age >= max_age:
#                             messages_to_delete.append(message)
#                     return messages_to_delete
#                 for doc in documents:
#                     try:
#                         channel_id = doc['channel_id']
#                         channel_name = doc['channel_name']
#                         channels_to_delete.append(f"{channel_id},{channel_name}")
#                         channel = self.bot.get_channel(int(channel_id))
#                         while True:
#                             messages = []
#                             message_delete=await delete_old_messages(channel=channel)
#                             messages.append(message_delete)
#                             print(messages)
#                             messages = message_delete
#                             if not messages:
#                                 break
#                             await channel.purge(bulk=True, check=check)
#                         await channel.send(f'{channel.name}삭제됨!', delete_after=1) 
#                     except:
#                         await channel.send(f'{channel.name}삭제오류!') 
#                         continue        
#                 await ctx.send('모든 채널 삭제완료!!', delete_after=1) 
#             else:
#                 await ctx.channel.send('권한이 없습니다', delete_after=1)
#         except Exception as e:
#             print(e)

#     @commands.hybrid_command ( name = '야옹이', with_app_command = True,description="15일지난 메시지제외 삭제" )
#     @commands.guild_only()
#     async def add_with_app_command(self, ctx: commands.Context, day=15):
#         if hasattr(ctx, 'interaction') and ctx.interaction is not None:
#             await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
#         await self.De_channel1(ctx,day=day)
            

# async def setup(bot):
#     await bot.add_cog(Del_num_all(bot), guilds=None) 
    
    
import discord
from discord import ui
from discord.ui import Button, View
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure, HybridCommand
import time
import os
import pymongo
from datetime import datetime, timedelta
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
from discord import Thread

class Del_num_all(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def delete_messages(channel):
        while True:
            messages = []
            async for message in channel.history(limit=99):
                if not isinstance(message, discord.MessageType.default):
                    messages.append(message)
            
            if not messages:
                break
            else:
                non_system_messages = [msg for msg in messages if msg.type == discord.MessageType.default]
                if not non_system_messages:
                    break
                    
                try:
                    await channel.delete_messages(non_system_messages)
                except discord.exceptions.Forbidden as e:
                    print(f"에러: {str(e)}, 메시지 삭제 실패")
                    break
            
    async def cat_channel_del(self, ctx, day):
        try:
            if ctx.author.guild_permissions.administrator:
                guild_id = str(ctx.guild.id)
                client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
                db = client['mydatabase']
                collection = db[guild_id]
                documents = collection.find()
                
                channels_to_delete = []
                for doc in documents:
                    try:
                        channel_id = doc['channel_id']
                        channel_name = doc['channel_name']
                        channels_to_delete.append(f"{channel_id},{channel_name}")
                        channel = self.bot.get_channel(int(channel_id))
                        current_date = ctx.message.created_at
                        
                        max_age = timedelta(days=day)
                        while True:
                            messages_to_delete = []

                            async for message in channel.history(limit=100):
                                message_age = current_date - message.created_at
                                if message_age < max_age:
                                    messages_to_delete.append(message)
                            if not messages_to_delete:
                                break
                            if messages_to_delete:
                                await channel.delete_messages(messages_to_delete)
                        await channel.send(f'{channel.name} 야옹!', delete_after=1)

                    except Exception as e:
                        print(f'{channel_name} 삭제 오류: {e}')
                        await channel.send(f'{channel.name} 삭제 오류!', delete_after=1)

                await ctx.send('모든 채널 야옹 완료!', delete_after=1)

            else:
                await ctx.send('권한이 없습니다', delete_after=1)

        except Exception as e:
            print(e)

        
        

    # @commands.command(name='고양이')
    # async def prx_add(self, ctx: commands.Context):
    #     await self.cat_channel_del(ctx)

    @commands.hybrid_command ( name = '야옹이', with_app_command = True,description="15일지난 메시지제외 삭제" )
    @commands.guild_only()
    async def add_with_app_command(self, ctx: commands.Context,day=15):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.cat_channel_del(ctx,day=day)

async def setup(bot):
    await bot.add_cog(Del_num_all(bot), guilds=None) 