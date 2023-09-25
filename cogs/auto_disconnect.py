import discord
from discord.ext import commands, tasks
from .auto_guild_nick import Auto_nick

class AutoDisconnect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auto_disconnect.start()
        self.nick = Auto_nick(bot)
    def cog_unload(self):
        self.auto_disconnect.cancel()

    async def is_bot_alone(self, vc):
        members = vc.members
        non_bots = [member for member in members if not member.bot]
        return len(non_bots) == 0

    @tasks.loop(seconds=10)  # 이 값을 조정하여 검사 간격을 변경할 수 있습니다.
    async def auto_disconnect(self):
        for vc in self.bot.voice_clients:
            if await self.is_bot_alone(vc.channel):
                    guild = vc.guild
                    print(guild.id)
                    member = await guild.fetch_member(self.bot.user.id)
                    try:
                        nick = self.bot.oriname[str(guild.id)]
                        await member.edit(nick=nick)
                    except:
                        await self.nick.get_nicknames()
                    if not str(guild.id) in self.bot.timer_runing:
                        self.bot.timer_runing[str(guild.id)]=False
                    self.bot.timer_runing[str(guild.id)]=False
                    print('러닝중')
                    await vc.disconnect()
                

    @auto_disconnect.before_loop
    async def before_auto_disconnect(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(AutoDisconnect(bot))
    # await bot.load_extension('cogs.auto_disconnect')


