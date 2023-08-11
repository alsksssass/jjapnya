import discord
from discord import ButtonStyle
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
from typing import Optional
from discord import Thread

# 나머지 코드는 동일하게 유지됩니다


# 나머지 코드는 동일하게 유지됩니다


# CustomView 클래스
class CustomView(View):
    def __init__(self, parent=None, timeout=None):
        super().__init__(timeout=timeout)
        self.parent = parent
        
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

        await self.message.edit(view=self)

class ChannelActionView(CustomView):
    def __init__(self, parent, channel_id, messages):
        super().__init__(timeout=None)
        self.parent = parent
        self.channel_id = channel_id
        self.messages = messages  # Set the 'messages' attribute
    async def on_add_button_click(self, interaction):
        
        target_channel = self.parent.bot.get_channel(int(self.channel_id))
        await self.parent.add_channel(interaction, target_channel, self.channel_id)
        
        if isinstance(target_channel, Thread):  # Check if the channel is a thread
            channel_type = "스레드"
        else:
            channel_type = "채널"
        await interaction.response.send_message(f'{target_channel.name}추가되었습니다.', delete_after=1)
        view = ChannelActionView(self.parent, self.channel_id, self.messages)
        view.add_item(AddButton(style=ButtonStyle.grey, disabled=True))
        view.add_item(DeleteButton())
        view.add_item(CleanButton())

        if str(target_channel.id) in self.messages:
            message = await interaction.channel.fetch_message(self.messages[str(target_channel.id)])
        else:
            message = await interaction.channel.send(content=f'{target_channel.name} {channel_type}', view=view)
            self.messages[str(target_channel.id)] = message.id

        await message.edit(content=f'{target_channel.name} {channel_type}', view=view)


    async def on_delete_button_click(self, interaction):
        # await interaction.response.send_message('삭제되었습니다.', delete_after=1)
        await self.parent.delete_channel(interaction, self.channel_id)
        target_channel = self.parent.bot.get_channel(int(self.channel_id))
        
        if isinstance(target_channel, Thread):  # Check if the channel is a thread
            channel_type = "스레드"
        else:
            channel_type = "채널"
        await interaction.response.send_message(f'{target_channel.name}삭제되었습니다.', delete_after=1)
        view = ChannelActionView(self.parent, self.channel_id, self.messages)
        view.add_item(AddButton())
        view.add_item(DeleteButton(disabled=True))
        view.add_item(CleanButton())

        if str(target_channel.id) in self.messages:
            message = await interaction.channel.fetch_message(self.messages[str(target_channel.id)])
        else:
            message = await interaction.channel.send(content=f'{target_channel.name} {channel_type}', view=view)
            self.messages[str(target_channel.id)] = message.id

        await message.edit(content=f'{target_channel.name} {channel_type}', view=view)

    async def on_clean_button_click(self, interaction):
        # await interaction.response.send_message('청소 시작 되었습니다.')
        await self.parent.clean_channel(interaction, self.channel_id)
        
        target_channel = self.parent.bot.get_channel(int(self.channel_id))

        # view = ChannelActionView(self.parent, self.channel_id, self.message)
        # channels_added = await self.parent.get_channels_in_db(interaction)
        # is_added = str(target_channel.id) in channels_added

        # add_button = AddButton()
        # delete_button = DeleteButton()

        # if is_added:
        #     add_button.style = ButtonStyle.grey
        #     add_button.disabled = True
        # else:
        #     delete_button.disabled = True

        # view.add_item(add_button)
        # view.add_item(delete_button)
        # view.add_item(CleanButton())

        # await self.message.edit(content=f'{target_channel.name} 채널 관리 시작', view=view)

class AddButton(Button):
    def __init__(self, style=ButtonStyle.green,**kwargs):
        super().__init__(style=style, label="추가")

    async def callback(self, interaction: discord.Interaction):
        await self.view.on_add_button_click(interaction)

class DeleteButton(discord.ui.Button):
    def __init__(self, disabled=False):  # 인수 'disabled'를 추가합니다.
        super().__init__(style=discord.ButtonStyle.red, label="제외", disabled=disabled)
    async def callback(self, interaction: discord.Interaction):
        await self.view.on_delete_button_click(interaction)

class CleanButton(Button):
    def __init__(self):
        super().__init__(style=ButtonStyle.red, label="청소")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message('청소 시작 되었습니다.', delete_after=1)
        await self.view.on_clean_button_click(interaction)

class CatButton(Button):
    def __init__(self):
        super().__init__(style=ButtonStyle.grey, label="고양이")
    
    async def callback(self, interaction: discord.Interaction):
        await self.view.clean_all_channels(interaction)

# CustomView 클래스 수정
class Channel_main_View(CustomView):
    def __init__(self, bot,parent, timeout=None):
        super().__init__(parent=parent, timeout=timeout)
        self.parent = parent
        self.bot=bot
        self.messages = {}  # 채널별 메시지 저장 (channel_id:message_id)
        self.add_item(CatButton())
    # 모든 등록된 채널 청소
    async def get_channels_in_db(self, guild_id):
        guild_id = str(guild_id)
        client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
        db = client['mydatabase']
        collection = db[guild_id]
        channels_result = collection.find({})
        return [channel['channel_id'] for channel in channels_result]

    async def clean_all_channels(self, interaction):
        await interaction.response.send_message('모든 채널이 청소되었습니다.', delete_after=1)
        guild_id = interaction.guild.id
        channels_in_db = await self.get_channels_in_db(guild_id)
        print(channels_in_db)
        for channel_id in channels_in_db:
            channel = self.bot.get_channel(int(channel_id))
                    # Delete messages in the channel until there are no more messages left
            if isinstance(channel, Thread):
                        await channel.purge(bulk=True)
                        await channel.send(f'{channel.name}삭제됨!', delete_after=1) 
            else:
                while True:
                    deleted = await channel.purge(limit=100)
                    if not deleted:
                        break
                        
                # await channel.purge(bulk=True)
            await interaction.channel.send(f'{channel.name} 청소완료', delete_after=1)
                
                
    


class Channel_list1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messages = {}
    async def is_channel_added(self, ctx, channel_id):
        guild_id = str(ctx.guild.id)
        client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
        db = client['mydatabase']
        collection = db[guild_id]

        existing_channel = collection.find_one({'channel_id': channel_id})
        return existing_channel is not None

    async def add_channel(self, ctx, target_channel, channel_id):
        if not await self.is_channel_added(ctx, channel_id):
            guild_id = str(ctx.guild.id)
            client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
            db = client['mydatabase']
            collection = db[guild_id]
            
            
            channel = target_channel
            collection.insert_one({
                'channel_id': str(channel_id),
                'channel_name': channel.name,
            })

    async def delete_channel(self, ctx, channel_id):
            guild_id = str(ctx.guild.id)
            client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
            db = client['mydatabase']
            collection = db[guild_id]
            
            collection.delete_one({'channel_id': str(channel_id)})

    async def clean_channel(self, ctx, channel_id):
        
            
            channel = self.bot.get_channel(int(channel_id))
            if isinstance(channel, Thread):
                await channel.purge(bulk=True)
                await ctx.channel.send(f'{channel.name}삭제됨!', delete_after=1) 
            else:
                while True:
                    deleted = await channel.purge(limit=100)
                    if not deleted:
                        break
                await ctx.channel.send(f'{channel.name}삭제됨!', delete_after=1)
            
        

    
    async def list_channels(self, ctx,target_channel, interaction=None):
        if ctx.author.guild_permissions.administrator or ctx.guild.id!=1134009736447148104:
            guild_id = str(ctx.guild.id)
            client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
            all_thread_channels = []
            for text_channel in ctx.guild.text_channels:
                all_thread_channels.extend(text_channel.threads)
            all_channels = ctx.guild.text_channels + ctx.guild.stage_channels + all_thread_channels
            
            # channel_names = [channel.name for channel in all_channels]
            # channels_added = await self.get_channels_in_db(ctx, channel_name=channel_names)
            
            views = []
            await ctx.send(content=f'{ctx.guild.name} 채널관리', view=Channel_main_View(bot=self.bot,parent=self))
            for index, channel in enumerate(all_channels):
                message = None  # 'message' 변수를 루프 시작 부분에서 None으로 초기화
                channels_added = await self.get_channels_in_db(ctx)

                is_added = str(channel.id) in channels_added

                add_button = AddButton()
                delete_button = DeleteButton()

                if is_added:
                    add_button.style = ButtonStyle.grey
                    add_button.disabled = True
                else:
                    delete_button.disabled = True

                channel_view = ChannelActionView(self, channel.id, self.messages)
                channel_view.add_item(add_button)
                channel_view.add_item(delete_button)
                channel_view.add_item(CleanButton())
                views.append(channel_view)
                
                
                

                
                if isinstance(channel, Thread):
                    channel_type = "스레드"
                else:
                    channel_type = "채널"
                message = await ctx.send(content=f'{channel.name} {channel_type}', view=channel_view)
                self.messages[str(channel.id)] = message.id
                



    async def get_channels_in_db(self, ctx):
        guild_id = str(ctx.guild.id)
        client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
        db = client['mydatabase']
        collection = db[guild_id]
        channels_result = collection.find({})
        return [channel['channel_id'] for channel in channels_result]

    @commands.hybrid_command ( name = '리스트1', with_app_command = True,description="채널청소관리 폼호출" )
    @commands.guild_only()
    async def list_all_channels(self, ctx):

        self.message = {}
        await self.list_channels(ctx, ctx.channel)

async def setup(bot):
    await bot.add_cog(Channel_list1(bot), guilds=None)
