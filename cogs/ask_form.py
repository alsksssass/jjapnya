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
import functools
from os.path import join

prev_sent_message = None
class Vote1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prev_sent_message=None
        self.commader=''     
        
    async def on_button_click(self,message, interaction):
            custom_id = interaction.data['custom_id']
            if custom_id in ["agree", "disagree"]:
                if custom_id == "agree":
                    result = "동의"
                else:
                    result = "거절"
                try:
                    guild = discord.utils.get(self.bot.guilds, id=975632483750137878)
                    channel = discord.utils.get(guild.channels, id=1133054105657548862)
                    if channel is not None:
                        if interaction.user.global_name:
                            name=interaction.user.global_name
                        else:
                            name=interaction.user.name
                        await channel.send(f"```{message}```\n건에 대하여\n{name}님이 {result}하였습니다.")
                    else:
                        raise ValueError("Invalid channel ID.")
                except Exception as e:
                    print(f"Error sending result message: {e}")

                await interaction.response.send_message(content=f"{result} 버튼을 누르셨습니다.")
                await interaction.message.delete() 
            
            
    @commands.command()
    async def 설문(self, ctx,*, message: str):
        
        user_ids = set()
        for guild in self.bot.guilds:
            # Send message to the guild owner
            user_ids.add(guild.owner.id)
            # Send message to the command user's channel

        # Remove duplicates from the set
        user_ids = list(set(user_ids))
            


        button_yes = Button(label='동의', style=discord.ButtonStyle.green, custom_id='agree')
        button_no = Button(label='반대', style=discord.ButtonStyle.red, custom_id='disagree')
        buttons = [button_yes, button_no]
        
        view = View(timeout=None)
        for value in buttons:
            value.callback =  functools.partial(self.on_button_click, message) 
            view.add_item(value)
        for guild in user_ids:
            user = self.bot.get_user(int(guild))
            print(user.global_name)
            try:
                if user.global_name:
                    name=user.global_name
                else:
                    name=user.name
                await user.send(f"{message}", view=view)
            except Exception as e:
                await ctx.send(f"Error sending message to {user.name}: {e}")

        

    # @commands.command(name='투표')
    # async def prx_add(self, ctx: commands.Context):
    #     await self.Vote_list(ctx)



async def setup(bot):
    await bot.add_cog(Vote1(bot), guilds=None) 
    
