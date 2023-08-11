import discord
from discord.ext import commands
import pymongo

class Gudock_list(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name='구독자')
    async def list_gudock(self, ctx):
        if ctx.author.id == 317655426868969482:
            client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
            db = client['gudock']
            collection = db['list']
            id_s = collection.find()
            
            # Create an empty string to store the results
            result_str = ""
            count=0
            for id_s_info in id_s:
                user_id = id_s_info.get('user_id')
                b_name = self.bot.get_user(user_id)
                result_str += f"유저이름: {b_name.global_name}, 유저 아이디: {user_id}\n"
                count+=1
            # Check if there are no channels in the collection
            if not result_str:
                await ctx.reply("구독자가 없습니다.", delete_after=10)
            else:
                await ctx.reply(f"구독자:\n{result_str}\n총{count}개", delete_after=10)

            # Rest of your code...
        else:
            await ctx.channel.send('권한이 없습니다', delete_after=1)
    @commands.command(name='서버리스트')
    async def list_gudock11(self, ctx):
        if ctx.author.id == 317655426868969482:
            client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
            db = client['list_out']
            collection = db['list']
            id_s = collection.find()
            
            # Create an empty string to store the results
            result_str = ""
            count=0
            for id_s_info in id_s:
                guild_id = id_s_info.get('guild_id')
                b_name = self.bot.get_guild(guild_id)
                result_str += f"길드이름: {b_name.name}, 유저 아이디: {b_name.owner.name}\n"
                count+=1
            # Check if there are no channels in the collection
            if not result_str:
                await ctx.reply("리스트가 없습니다..", delete_after=10)
            else:
                await ctx.reply(f"리스트:\n{result_str}\n총{count}개", delete_after=10)

            # Rest of your code...
        else:
            await ctx.channel.send('권한이 없습니다', delete_after=1)
    
    # ... your other commands ...
    @commands.command(name='구독공지')
    async def list_gudock1(self, ctx,*,content):
        if ctx.author.id == 317655426868969482:
            # Establish a connection to the MongoDB database
            client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
            db = client['gudock']
            collection = db['list']
            id_s = collection.find()

            # Create an empty string to store the results
            result_str = ""
            count = 0

            for id_s_info in id_s:
                user_id = id_s_info.get('user_id')
                b_name = self.bot.get_user(user_id)

                # Send a DM to the user
                try:
                    user = await self.bot.fetch_user(user_id)
                    await user.send(content)
                    result_str += f"성공!!유저이름: {b_name.global_name}, 유저 아이디: {user_id}\n"
                except discord.Forbidden:
                    result_str += f"실패!!유저이름: {b_name.global_name}, 유저 아이디: {user_id}\n"
                    await ctx.reply(f"Failed to send DM to {user_id},{user.name}{user.global_name}.")

                count += 1

            # Check if there are no channels in the collection
            if not result_str:
                await ctx.reply("구독자가 없습니다.", delete_after=10)
            else:
                await ctx.reply(f"구독자:\n{result_str}\n총 {count}개", delete_after=10)

        else:
            await ctx.channel.send('권한이 없습니다', delete_after=1)
async def setup(bot):
    await bot.add_cog(Gudock_list(bot), guilds=None)
