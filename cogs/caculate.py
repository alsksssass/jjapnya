import discord
from discord.ext import commands, tasks


class Caculate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def calculate_expression(self,expression: str) -> float:
        expression = expression.replace('^', '**')
        cleaned_expr = ''.join(c for c in expression if c.isdigit() or c in ['+', '-', '*', '/', '.', '(', ')', '**'])
        result = eval(cleaned_expr)
        return result
    
    @commands.hybrid_command ( name = '계산',aliases=['='], with_app_command = True,description="계산기('+', '-', '*', '/', '.', '(', ')', '**')" )
    async def calculate(self,ctx, *, expression: str):
        try:
            result = self.calculate_expression(expression)
            await ctx.send(f'결과: {result}')
        except Exception as e:
            await ctx.send(f'계산 중 오류가 발생했습니다: {e}')
    








async def setup(bot):
    await bot.add_cog(Caculate(bot)) ##길드 아이디 입력