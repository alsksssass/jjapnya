import discord
from discord.ext import commands

class Notice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_guild_id = 975632483750137878
    async def module(self, ctx, content: str):
        if ctx.author.id == 317655426868969482:
            user_ids = set()
            for guild in self.bot.guilds:
                # Send message to the guild owner
                user_ids.add(guild.owner.id)
                # Send message to the command user's channel

            # Remove duplicates from the set
            user_ids = list(set(user_ids))
            
            for user_id in user_ids:
                user = self.bot.get_user(user_id)
                try:
                    await user.send(f'{content}')
                except Exception as e:
                    await ctx.send(f"Error sending message to user {user_id}: {str(e)}")
            
            count = len(user_ids)
            await ctx.send(f'{count}명 에게 전송완료')
            
    # @commands.command(name='공지')
    # async def prefix(self,ctx: commands.Context,*args):
    #     a=args[0:]
    #     content=' '.join(s for s in a)
    #     await self.module(ctx,content)

                
    @commands.command()
    async def 공지(self, ctx: commands.Context,*,content:str):
            await self.module(ctx,content)


async def setup(bot):
    await bot.add_cog(Notice(bot)) ##길드 아이디 입력