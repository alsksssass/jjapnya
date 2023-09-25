import discord
from discord.ext import commands, tasks
import asyncio
from collections import Counter
import pymongo


client = pymongo.MongoClient("mongodb+srv://catbot:SpFdAzUyBgtzjeLk@cluster0.bcdpa56.mongodb.net/?retryWrites=true&w=majority")
db = client['list_out']
collection = db['list']

class Autostaterm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.change_status.start()
    
    # def find_most_common_values(self):
    #     user_ids = []
    #     for guild in self.bot.guilds:
    #         # Send message to the guild owner
    #         user_ids.append(guild.owner.id)
    #     # Count the elements in the user_ids set and store them in a dictionary
    #     counts = Counter(user_ids)

    #     # Get the most common values and their counts
    #     most_common_values = [(value, count) for value, count in counts.most_common(3)]

    #     return most_common_values



    @tasks.loop(seconds=60)
    async def change_status(self):
        await self.bot.wait_until_ready()
        subscribed_guild_ids = [doc['guild_id'] for doc in collection.find({'guild_id': {'$exists': True}})]
        user_ids = []
        for guild in self.bot.guilds:
            # Only consider non-subscribed guilds
            if guild.id not in subscribed_guild_ids:
                # Send message to the guild owner
                user_ids.append(guild.owner.id)

        counts = Counter(user_ids)
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)

        result = []
        top_counts = [sorted_counts[i][1] for i in range(3)]

                    
        for value, count in sorted_counts:
            if count in top_counts:
                result.append((value, count))

        total_guilds=len(self.bot.guilds)
        num=len(result)
        count1 = len(self.bot.guilds)-len(subscribed_guild_ids)
        status_list = [
            # f'Made by 변상훈',
            f'추가제한까지 {total_guilds}/100',
            f'!귀여워 0.31 stable',
            '타로마스터 자동화 무료!',
            '!타로마스터 를 쳐보세요!',
            f'{count1}건 조사보조',
        ]
        previous_count = -1
        current_rank = 0
        for value, count in result:
            if count != previous_count:
                current_rank += 1
            previous_count = count

            b_name = self.bot.get_user(value)
            if b_name.global_name is None:
                nick_b = b_name.name
            else:
                nick_b = b_name.global_name

            status_list.append(f'{current_rank}위 {nick_b}님 {count}건 크씬진행')
        for guild in self.bot.guilds:
            for vc in guild.voice_channels:
                if vc.members:
                    if len(vc.members) >= 4:
                        # print(len(vc.members))
                        # print(vc.members)
                        status_list.append(f"Now!{guild.name} 진행")
                    else:
                        pass
        all_user_ids = []
        for guild in self.bot.guilds:
            # Only consider non-subscribed guilds
            if guild.id not in subscribed_guild_ids:
                user_ids = [member.id for member in guild.members if member.id != guild.owner_id and member.id != self.bot.user.id]
                all_user_ids.extend(user_ids)

        # Count the occurrences of each user ID
        user_counts = Counter(all_user_ids)
        
        # Get the top 3 most common user IDs
        top_3 = user_counts.most_common(3)
        
        # Check for ties and include them in the top 3
        tied_users = [user for user, count in user_counts.items() if count == top_3[-1][1] and user not in [x[0] for x in top_3]]
        top_3.extend([(user, top_3[-1][1]) for user in tied_users])
        
        # Print the results
        # status_list.append(f"{count1}건중 최다 플레이어:")
        for i, (user_id, count) in enumerate(top_3):
            # Get the global name of the user
            user = await self.bot.fetch_user(user_id)
            global_name = f"{user.global_name}"
            
            status_list.append(f"{i+1}위.{global_name}, {count}/{count1}회플레이")
        for i in range(len(status_list)):
            await self.bot.change_presence(activity=discord.Game(name=status_list[i]))

            await asyncio.sleep(10)
        # await self.bot.change_presence(activity=discord.Game(name=status_list[0]))
                

async def setup(bot):
    await bot.add_cog(Autostaterm(bot))
    # await bot.load_extension('cogs.auto_disconnect')


