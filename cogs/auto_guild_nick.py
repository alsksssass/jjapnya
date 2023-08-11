import discord
from discord.ext import commands, tasks
import asyncio
from collections import Counter
import pymongo
import re

def identify_time_string(time_string):
    time_pattern = r'^\d{2}시간\d{2}분\d{2}초$'
    match = re.match(time_pattern, time_string)
    if match:
        return True
    return False
class Auto_nick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        await self.get_nicknames()

    async def get_nicknames(self):
        for guild in self.bot.guilds:
            member = guild.get_member(self.bot.user.id)
            current_nickname = member.nick
            if current_nickname ==None:
                current_nickname='짭냥'
            if identify_time_string(str(current_nickname)):
                current_nickname='짭냥'
            self.bot.oriname[str(guild.id)]=None
            self.bot.oriname[str(guild.id)] = current_nickname
        print(self.bot.oriname)

                

async def setup(bot):
    await bot.add_cog(Auto_nick(bot))
    # await bot.load_extension('cogs.auto_disconnect')


