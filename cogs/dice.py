import discord
from discord.ext import commands, tasks
import random

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.hybrid_command ( name = 'r',aliases=['ㄱ'], with_app_command = True,description="주사위" )
    async def roll(self,ctx, sides: int = 6, count: int = 1):
        if sides < 1 or count < 1:
            await ctx.send("주사위의 면 수와 갯수는 1 이상이어야 합니다.")
            return

        results = [random.randint(1, sides) for _ in range(count)]
        total = sum(results)
        result_str = ', '.join(map(str, results))
        
        await ctx.send(f'{ctx.author.global_name}님, {count}개의 {sides}면 주사위 결과: {result_str} 총합 : {total}')

        








async def setup(bot):
    await bot.add_cog(Dice(bot)) ##길드 아이디 입력