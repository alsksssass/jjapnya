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

class C_list(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def show_list(self,ctx):
        guild = discord.utils.get(self.bot.guilds, id=self.bot.guild_id)
        channel = discord.utils.get(guild.channels, id=self.bot.channel_id)
        await channel.send(f'{ctx.author.name}님이{ctx.guild.name}에서 캐릭터 명령어 사용')
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
                
                async def button_callback(interaction):
                    button_id = interaction.data['custom_id']
                    await interaction.response.send_message(f'{button_id}역의 {interaction.user.name} 님이 준비되었습니다.', delete_after=1)
                    button_dict[button_id].disabled=True
                    button_dict[button_id].label=f'{interaction.user.name} 님이 선택.'
                    add=ctx.author
                    
                    member = ctx.guild.get_member(interaction.user.id)
                    await member.edit(nick=button_id)
                    # # print(channels_nick_name.disabled)
                    await a.edit(content=f'```{ctx.guild.name} 에 오신것을 환영합니다. \n캐릭터 롤을 선택하세요! 닉네임이 변경됩니다.```',view=view)

                
                for nick_name in channels_nick_name:
                    button_dict[nick_name] = Button(label=nick_name, style = discord.ButtonStyle.green, custom_id=nick_name)
                    # view.add_item(button_dict[channels_nick_name.index(nick_name)])
                    button_list.append(button_dict[nick_name])
                    
                view = View(timeout=None)
                for value in button_dict.values():
                    value.callback = button_callback
                    view.add_item(value)
                a=await ctx.channel.send(content=f'```{ctx.guild.name} 에 오신것을 환영합니다. \n캐릭터 롤을 선택하세요! 닉네임이 변경됩니다.```',view=view)

            else:
                await ctx.channel.send('권한이 없습니다', delete_after=1)
        except Exception as e:
            await ctx.send('오류발생시 ``!닉초기화`` 명령어 사용후 다시 추가해 주세요!')
            await ctx.send('이모지 사용시 오류가 납니다. !@#-특문한글영어문자만 사용해주세요')
        
        

    @commands.command(name='캐릭터')
    async def prx_add(self, ctx: commands.Context):
        await self.show_list(ctx)

    @commands.hybrid_command ( name = '캐릭터_', with_app_command = True,description="닉네임 변경폼을 호출합니다." )
    @commands.guild_only()
    async def add_with_app_command(self, ctx: commands.Context):
        await ctx.interaction.response.send_message(content='캐릭터_명령어 사용됨',delete_after=0.000000001,ephemeral=True,silent=True)
        await self.show_list(ctx)

async def setup(bot):
    await bot.add_cog(C_list(bot), guilds=None) 