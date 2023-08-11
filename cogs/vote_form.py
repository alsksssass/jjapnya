import discord
from discord import ui
from discord.ui import Button, View
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure, HybridCommand
import time
import os
import pymongo
from datetime import datetime
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
import aiohttp

prev_sent_message = None
class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prev_sent_message=None
        self.result_message=[]
        self.commader=''
    async def Vote_list(self,ctx):
        self.prev_sent_message=None
        try:
            if ctx.author.guild_permissions.administrator:
                guild_id = str(ctx.guild.id)
                client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
                db = client['nickdatabase']
                collection = db[guild_id]
                # Get the guild ID
                # Read the list of channel IDs and names from the file
                # with open(f'{guild_id}_channels.txt', 'r') as f:
                documents = collection.find()
                button_list=[]
                button_dict={} 
                # Create a list of channel IDs and names from the documents
                channels_nick_name = []
                
                for doc in documents:
                    nickname = doc['nick_name']
                    result = ''.join(nickname)
                    channels_nick_name.append(str(result))                
                channels_nick_name.append('?. 기타')
                user_votes = {nick_name: [] for nick_name in channels_nick_name}
                channels_nick_name.append('종료')
                
                message_content=f'```{ctx.guild.name} 의 투표입니다. 생각하시는 범인을 투표해 주세요!```\n```!주의!\n투표는 종료 전까지 언제든지 다시 버튼을눌러 재투표가 가능합니다.```\n```너무 마구잡이로 누르면 투표에 오류가 생길수 있으니 신중하게 눌러주세요.```\n```진행자가 종료버튼을 누르면 더이상 투표가 불가능 합니다.```\n```기타는 투표기능 자체에 포함되어 있으므로 필요하지 않은 크라임씬이 있을수 있습니다.```'
                async def button_callback(interaction):
                    global prev_sent_message
                    
                    button_id = interaction.data['custom_id']
                    if button_id == "종료":
                        if interaction.user.guild_permissions.administrator:
                            for button in button_dict.values():  # 버튼들을 순환하며 비활성화
                                button.disabled = True
                            await a.edit(content=message_content,view=view)
                            return await interaction.response.send_message(f'투표가 종료되었습니다.')    
                        
                        else:
                            await interaction.response.send_message(f'관리자가 아닙니다.', delete_after=1)    
                    await interaction.response.send_message(f'{interaction.user.nick}님이 투표하셧습니다.', delete_after=1)
                    for key, value in user_votes.items():
                        if interaction.user.nick in value:
                            value.remove(interaction.user.nick)

                # 새로운 목록에 사용자를 추가합니다.
                    user_votes[button_id].append(interaction.user.nick)
                    self.result_message.clear()
                    self.result_message.append('투표 결과입니다.')
                    total=0
                    for nick_name, votes in user_votes.items():
                        self.result_message.append(f"```{nick_name}: {votes} {len(votes)} 표```")
                        total+=len(votes)
                    # await ctx.author.send("\n".join(result_message))
                    prev_sent_message=self.prev_sent_message
                    
                    if prev_sent_message is None:
                        
                        acc=await self.bot.fetch_user(self.commader)
                        
                        self.prev_sent_message = await acc.send("\n".join(self.result_message))
                        # autor_id=client.get_user(int(self.commader))
                        # self.prev_sent_message =await autor_id.send("\n".join(self.result_message))
                        # self.prev_sent_message = autor_id.send("\n".join(self.result_message))
                        # self.prev_sent_message = await interaction.command.send("\n".join(self.result_message))
                            
                    else:
                        await prev_sent_message.edit(content="\n".join(self.result_message))
                    
                    if total>=(len(channels_nick_name)-2):
                        await ctx.send('모든 플레이어가 투표를 완료 하였습니다.\n진행자는 종료 버튼을 눌러 투표를 종료해 주세요!!')
                        self.bot.all_p = self.result_message
                for nick_name in channels_nick_name:
                    if nick_name in channels_nick_name[-1]:
                        button_dict[nick_name] = Button(label=nick_name, style=discord.ButtonStyle.red, custom_id=nick_name)
                    elif nick_name in channels_nick_name[-2]:
                        button_dict[nick_name] = Button(label=nick_name, style=discord.ButtonStyle.primary, custom_id=nick_name)
                    else:
                        button_dict[nick_name] = Button(label=nick_name, style = discord.ButtonStyle.green, custom_id=nick_name)
                        # view.add_item(button_dict[channels_nick_name.index(nick_name)])
                        button_list.append(button_dict[nick_name])
                
                # end_button = Button(label="!종료!", style=discord.ButtonStyle.red, custom_id="종료")
                # button_list.append(end_button)
                self.commader=ctx.author.id
                view = View(timeout=None)
                for value in button_dict.values():
                    value.callback = button_callback
                    view.add_item(value)
                
                a=await ctx.channel.send(content=message_content,view=view)
                
            else:
                await ctx.channel.send('권한이 없습니다', delete_after=1)
        except Exception as e:
            print(e)
            await ctx.send('오류발생시 ``!닉초기화`` 명령어 사용후 다시 추가해 주세요!')
            await ctx.send('이모지 사용시 오류가 납니다. !@#-특문한글영어문자만 사용해주세요')
        
        

    # @commands.command(name='투표')
    # async def prx_add(self, ctx: commands.Context):
    #     await self.Vote_list(ctx)

    @commands.hybrid_command ( name = '투표', with_app_command = True,description="투표폼을 호출합니다." )
    @commands.guild_only()
    async def add_with_app_command(self, ctx: commands.Context):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.Vote_list(ctx)

async def setup(bot):
    await bot.add_cog(Vote(bot), guilds=None) 
    
