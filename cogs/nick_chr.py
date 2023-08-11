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
import discord.errors

class C_list(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def show_list(self,ctx):
        
        try:
            if not ctx.author.guild_permissions.administrator:
                    await ctx.channel.send('권한이 없습니다.', delete_after=1)
                    
                    return
            global i_num
            guild_id = str(ctx.guild.id)
            client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
            db = client['nickdatabase']
            collection = db[guild_id]
            
            
            documents = collection.find()
            button_list=[]
            button_dict={} 
            # Create a list of channel IDs and names from the documents
            rolls_dict = {}
            channels_nick_name = []
            roll_exists = any(["roll" in doc for doc in documents])
            if roll_exists:
                
                
                # # Get the guild ID
                # # Read the list of channel IDs and names from the file
                # # with open(f'{guild_id}_channels.txt', 'r') as f:
                # documents = collection.find()
                # button_list=[]
                # button_dict={} 
                # # Create a list of channel IDs and names from the documents
                # rolls_dict = {}
                documents1 = collection.find()
                for doc in documents1:
                    nickname = doc['nick_name']
                    
                    result = ''.join(nickname)
                    roll = doc['roll']  # Get the roll from the document
                    rolls_dict[result] = roll  # Store the roll using the nickname in the rolls_dict
                    
                    # result = ''.join(nickname)
                    # channels_nick_name.append(str(result))               
                
                i_num=0
                async def button_callback(interaction):
                    global i_num
                    nick_n=self.bot.get_user(int(interaction.user.id))
                    button_id = interaction.data['custom_id']
                    await interaction.response.send_message(f'{button_id}역의 {nick_n.display_name} 님이 준비되었습니다.', delete_after=1)
                    button_dict[button_id].disabled=True
                    
                    button_dict[button_id].label=f'{nick_n.display_name} 님이 선택.'
                    add=ctx.author
                    total=len(button_list)
                    member = ctx.guild.get_member(interaction.user.id)
                    await member.edit(nick=button_id)
                    # # print(channels_nick_name.disabled)
                    await a.edit(content=f'```{ctx.guild.name} 에 오신것을 환영합니다. \n캐릭터 롤을 선택하세요! 닉네임이 변경됩니다.```',view=view)
                    i_num+=1
                    user_info=(button_id, interaction.user.id)
                    role_name = rolls_dict[button_id]
                    if role_name is not None:
                        role = discord.utils.get(ctx.guild.roles, name=role_name)
                        if role:
                            await member.add_roles(role)
                        else:
                            await ctx.send(f'오류: 역할 {role_name}을 찾을 수 없습니다.')
                    
                    self.bot.player_l.append(user_info)
                    if i_num >= total:
                        self.bot.all_p = True
                        print(total)
                        print(i_num)
                        return
                    
                
                for nick_name in rolls_dict.keys():
                    button_dict[nick_name] = Button(label=nick_name, style=discord.ButtonStyle.green, custom_id=nick_name)
                    button_list.append(button_dict[nick_name])
                    
                view = View(timeout=None)
                for value in button_dict.values():
                    value.callback = button_callback
                    view.add_item(value)
                a=await ctx.channel.send(content=f'```{ctx.guild.name} 에 오신것을 환영합니다. \n캐릭터 롤을 선택하세요! 닉네임이 변경되고 롤이 주어집니다.```',view=view)
            else:
                
                
                # # Get the guild ID
                # # Read the list of channel IDs and names from the file
                # # with open(f'{guild_id}_channels.txt', 'r') as f:
                # documents = collection.find()
                # button_list=[]
                # button_dict={} 
                # # Create a list of channel IDs and names from the documents
                # channels_nick_name = []
                documents1 = collection.find()
                for doc in documents1:
                    nickname = doc['nick_name']
                    result = ''.join(nickname)
                    channels_nick_name.append(str(result))                
                
                i_num=0
                async def button_callback(interaction):
                    global i_num
                    nick_n=self.bot.get_user(int(interaction.user.id))
                    button_id = interaction.data['custom_id']
                    await interaction.response.send_message(f'{button_id}역의 {nick_n.display_name} 님이 준비되었습니다.', delete_after=1)
                    button_dict[button_id].disabled=True
                    
                    button_dict[button_id].label=f'{nick_n.display_name} 님이 선택.'
                    
                    add=ctx.author
                    total=len(button_list)
                    member = ctx.guild.get_member(interaction.user.id)
                    await member.edit(nick=button_id)
                    # # print(channels_nick_name.disabled)
                    await a.edit(content=f'```{ctx.guild.name} 에 오신것을 환영합니다. \n캐릭터 롤을 선택하세요! 닉네임이 변경됩니다.```',view=view)
                    i_num+=1
                    user_info=(button_id, interaction.user.id)
                    
                    self.bot.player_l.append(user_info)
                    if total >= i_num:
                        self.bot.all_p = True
                        return
                    
                
                for nick_name in channels_nick_name:
                    button_dict[nick_name] = Button(label=nick_name, style = discord.ButtonStyle.green, custom_id=nick_name)
                    # view.add_item(button_dict[channels_nick_name.index(nick_name)])
                    button_list.append(button_dict[nick_name])
                    
                view = View(timeout=None)
                for value in button_dict.values():
                    value.callback = button_callback
                    view.add_item(value)
                a=await ctx.channel.send(content=f'```{ctx.guild.name} 에 오신것을 환영합니다. \n캐릭터 롤을 선택하세요! 닉네임이 변경됩니다.```',view=view)
                    
        except discord.errors.Forbidden as e:
            print(e)
            await ctx.send("봇의 역할을 맨위로 옮겨주세요. 봇의 권한이 낮습니다.")
        except Exception as e:
            print(e)
            await ctx.send('오류발생시 ``!닉초기화`` 명령어 사용후 다시 추가해 주세요!')
            await ctx.send('이모지 사용시 오류가 납니다. !@#-특문한글영어문자만 사용해주세요')
        
        

    # @commands.command(name='캐릭터')
    # async def prx_add(self, ctx: commands.Context):
    #     await self.show_list(ctx)

    @commands.hybrid_command ( name = '캐릭터', with_app_command = True,description="닉네임 변경폼을 호출합니다." )
    @commands.guild_only()
    async def add_with_app_command(self, ctx: commands.Context):
        if hasattr(ctx, 'interaction') and ctx.interaction is not None:
            await ctx.send(content='https://i.imgur.com/gk3iHuX.gif',delete_after=0.00001)
        await self.show_list(ctx)

async def setup(bot):
    await bot.add_cog(C_list(bot), guilds=None) 