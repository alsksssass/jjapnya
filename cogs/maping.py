import discord
from discord.ext import commands, tasks
import socket
import random
import string
import pymongo
from discord.ui import Button, View,Select
from bson import ObjectId
from collections import Counter
import asyncio
from asyncio import sleep
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
# import logging
import io
import discord
from discord.ext import commands
from PIL import Image

image_path = './map/map.jpg'  # 이미지 경로를 설정하세요. 예: 'image.jpg'
x, y = 0, 0
max_x, max_y = 100, 100  # 최대 x, y 값을 설정하세요.

class Mapping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.msg={}
        self.channel_id={}
    def update_image(self, x, y):
        img = Image.open(image_path)
        cropped_img = img.crop((x, y, x + 200, y + 200))  # 이 크기는 필요에 따라 조절하세요.

        buf = io.BytesIO()
        cropped_img.save(buf, format="JPEG")
        buf.seek(0)
        discord_image = discord.File(fp=buf, filename="image.jpg")

        return discord_image, buf
    async def on_button_click(self, interaction):
        global x, y
        guild_id = str(interaction.guild.id)
        image_path = './map/map1.jpg'
        clicked_button_id = interaction.data['custom_id']
        
        if clicked_button_id == f'{guild_id}up':
            y = max(0, y - 1)
        elif clicked_button_id == f'{guild_id}down':
            y = min(max_y, y + 1)
        elif clicked_button_id == f'{guild_id}left':
            x = max(0, x - 1)
        elif clicked_button_id == f'{guild_id}right':
            x = min(max_x, x + 1)

        img, buf = self.update_image(x, y)
        await interaction.message.edit(attachments=discord.File(img))
        buf.close()

    async def mapping(self, ctx):
        global x, y

        # 버튼 생성
        guild_id = str(ctx.guild.id)
        buttons = [
            discord.ui.Button(style=discord.ButtonStyle.primary, emoji="⬆️", custom_id=f'{guild_id}up'),
            discord.ui.Button(style=discord.ButtonStyle.primary, emoji="⬇️", custom_id=f'{guild_id}down'),
            discord.ui.Button(style=discord.ButtonStyle.primary, emoji="➡️", custom_id=f'{guild_id}right'),
            discord.ui.Button(style=discord.ButtonStyle.primary, emoji="⬅️", custom_id=f'{guild_id}left')
        ]
        view = View(timeout=None)
        for value in buttons:
            value.callback = self.on_button_click
            view.add_item(value)
        img, buf = self.update_image(x, y)
        msg = await ctx.send(view=view, file=img)
        self.msg[guild_id] = [str(msg.id)]
        self.channel_id[guild_id] = []
        self.channel_id[guild_id].append(f'{ctx.channel.id}')
        buf.close()


    @commands.command(name='이미지')
    async def send_image(self,ctx):
        await self.mapping(ctx)






async def setup(bot):
    await bot.add_cog(Mapping(bot))