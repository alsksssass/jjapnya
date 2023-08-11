import discord
from discord.ext import commands
import asyncio
from asyncio import sleep

round = 1
# mesh = {"가": [0, "IMG_1037.jpg", "IMG_1038.jpg", "IMG_1039.jpg"],"나": [0, "IMG_1040.jpg", "IMG_1041.jpg", "IMG_1042.jpg"],"다": [0, "IMG_1043.jpg", "IMG_1044.jpg", "IMG_1045.jpg"]}
mesh = { 
        "가": [0, "https://i.imgur.com/3jkLpaA.jpg", "https://i.imgur.com/zAriocC.jpg", "https://i.imgur.com/yZmLkOI.jpg"],
        "나": [0, "https://i.imgur.com/JUnkJ84.jpg", "https://i.imgur.com/XZeSioe.jpg", "https://i.imgur.com/iDMSGEE.jpg"],
        "다": [0, "https://i.imgur.com/3LQ00v1.jpg", "https://i.imgur.com/bH2zZ0D.jpg", "https://i.imgur.com/VlxgTHy.jpg"],
        "라": [0, "https://i.imgur.com/LYtDWQA.jpg", "https://i.imgur.com/0HW2fxl.jpg", "https://i.imgur.com/DEOztDE.jpg"],
        "마": [0, "https://i.imgur.com/iuNeG85.jpg", "https://i.imgur.com/qXsgdTO.jpg", "https://i.imgur.com/PdPUOtf.jpg"],
        "바": [0, "https://i.imgur.com/IkZ8nAE.jpg", "https://i.imgur.com/jjnWSo5.jpg", "https://i.imgur.com/lyk4BZx.jpg"],
        "사": [0, "https://i.imgur.com/e75EqQw.jpg", "https://i.imgur.com/Z9TgsH8.jpg", "https://i.imgur.com/ku9Z9sn.jpg"],
        "아": [0, "https://i.imgur.com/poHUi7g.jpg", "https://i.imgur.com/9gdeSIk.jpg", "https://i.imgur.com/pgETvGC.jpg"],
        "자": [0, "https://i.imgur.com/vInnjuS.jpg", "https://i.imgur.com/HGxbkiF.jpg", "https://i.imgur.com/l0ARKIe.jpg"],
        "차": [0, "https://i.imgur.com/WS2j6MI.jpg", "https://i.imgur.com/6sKmnpu.jpg", "https://i.imgur.com/GAVbXaT.jpg"],
        "카": [0, "https://i.imgur.com/ecHTx7P.jpg", "https://i.imgur.com/D2Yru3c.jpg", "https://i.imgur.com/Spfk6E4.jpg"],
        "타": [0, "https://i.imgur.com/UyzWm8S.jpg", "https://i.imgur.com/2CddKYj.jpg", "https://i.imgur.com/8JBeNkg.jpg"],
        "파": [0, "https://i.imgur.com/yI8WiFo.jpg", "https://i.imgur.com/5QCyAU9.jpg", "https://i.imgur.com/AycJTHs.jpg"],
        "하": [0, "https://i.imgur.com/cR9qLgI.jpg", "https://i.imgur.com/2D8T1qm.jpg", "https://i.imgur.com/HOfRx4D.jpg"],
        "숲": [0, "https://i.imgur.com/PiDoLjR.jpg", "https://i.imgur.com/3Oxqxqe.jpg", "https://i.imgur.com/c2cGkux.jpg"],
        "앵무": [0, "https://i.imgur.com/1wd8AYC.jpg", "https://i.imgur.com/x6knO8g.jpg", "https://i.imgur.com/RGxpOvt.jpg"],
        "연행": [0, "https://i.imgur.com/fETyKL7.jpg", "https://i.imgur.com/7r4Fq9K.jpg", "https://i.imgur.com/98ZVfwj.jpg"],
        "라1": [0, "https://i.imgur.com/LYtDWQA.jpg", "https://i.imgur.com/0HW2fxl.jpg", "https://i.imgur.com/DEOztDE.jpg"],
        "라2": [0, "https://i.imgur.com/LYtDWQA.jpg", "https://i.imgur.com/0HW2fxl.jpg", "https://i.imgur.com/DEOztDE.jpg"],
        "라3": [0, "https://i.imgur.com/LYtDWQA.jpg", "https://i.imgur.com/0HW2fxl.jpg", "https://i.imgur.com/DEOztDE.jpg"],}


class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def module(self,ctx):
        await ctx.channel.send('ping')
    
    @commands.command()
    async def 단서(self,ctx,name:str):
        if ctx.guild.id == 333978548245233667:
            if not ctx.author.guild_permissions.administrator:
                await ctx.send('권한이 없습니다', delete_after=1)
                return
            global round ,mesh
            content= mesh[name][round]
            # abs = await ctx.send(content='-',file=discord.File(f'./img/{content}'))
            embed = discord.Embed(color=696969)

            # Add an image to the embed
            embed.set_image(url=content)
            # Edit the message content to the value stored in the "round" index
            # await message.edit(content='-',file= discord.File(f'./img/{value[round]}'))
            
            
            channel = self.bot.get_channel(1082628286540165120)
            abs=await channel.send(embed=embed)
            # abs = await ctx.send(content)
            
            abr=abs.id
            print(abr)
            mesh[f"{name}"][0] = abr

            # zeroth_values = [mesh[key][0] for key in mesh if mesh[key][0] != 0]
            
    @commands.command()
    async def 초기화(self,ctx):
        if ctx.guild.id == 333978548245233667:
            if not ctx.author.guild_permissions.administrator:
                await ctx.send('권한이 없습니다', delete_after=1)
                return

        global round, mesh

        # Update the value0 of all keys to 0
        for key in mesh:
            mesh[key][0] = 0
        print(mesh)
        round = 1

        await ctx.send('초기화 됨', delete_after=5)


        
    @commands.command()
    async def 목록(self,ctx):
        if ctx.guild.id == 333978548245233667:
            if not ctx.author.guild_permissions.administrator:
                await ctx.send('권한이 없습니다', delete_after=1)
                return
            global round

            # Create a new dictionary "result" that only includes the items in "mesh"
            # where the first value (at index 0) is not 0
            

            # Loop through all items in "mesh"
            for key, value in mesh.items():
                # If the first value is not 0 and the second value (at index 1) is in "result"
                    # Fetch the message with the message ID stored in the third value (at index 2)
                    
                    # Edit the message content to the value stored in the "round" index
                    # await message.edit(content='-',file= discord.File(f'./img/{value[round]}'))
                    # await ctx.send(f'{key}{value[round]}')# Create a new embed message
                    embed = discord.Embed(title=f'{key} {value[round]}', color=696969)

                    # Add an image to the embed
                    embed.set_image(url=value[round])

                    # Add the URLs as clickable fields in the embed
                    # for i in range(2, len(value)):
                    #     embed.add_field(name=f'URL {i-1}:', value=value[i], inline=False)

                    # Send the embed message
                    await ctx.send(embed=embed)
                    await asyncio.sleep(0.5)


    @commands.command()
    async def 라운드(self,ctx,name:int):
        if ctx.guild.id == 333978548245233667:
            if not ctx.author.guild_permissions.administrator:
                await ctx.send('권한이 없습니다', delete_after=1)
                return
            global round
            round = name
            
            # Create a new dictionary "result" that only includes the items in "mesh"
            # where the first value (at index 0) is not 0
            result = {key: value for key, value in mesh.items() if value[0] != 0}

            # Loop through all items in "mesh"
            for key, value in result.items():
                # If the first value is not 0 and the second value (at index 1) is in "result"
                    # Fetch the message with the message ID stored in the third value (at index 2)
                    other_channel = self.bot.get_channel(1082628286540165120)
                    message = await other_channel.fetch_message(value[0])
                    embed = discord.Embed(color=696969)

                    # Add an image to the embed
                    embed.set_image(url=value[round])
                    # Edit the message content to the value stored in the "round" index
                    # await message.edit(content='-',file= discord.File(f'./img/{value[round]}'))
                    
                    await message.edit(embed=embed)
                    # await message.edit(value[round])
                    await asyncio.sleep(1)
            await ctx.send('변경완료')

                
    # @commands.hybrid_command ( name = 'ping', with_app_command = True,description="현재 채널에 기록된 셋팅내용을 삭제합니다." )
    # @commands.guild_only()
    # async def slash_with_app_command(self, ctx: commands.Context):
    #         await ctx.interaction.response.send_message(content=f'ping_명령어 사용됨',delete_after=0.000000001,ephemeral=True,silent=True)
    #         await self.module(ctx)


async def setup(bot):
    await bot.add_cog(ping(bot)) ##길드 아이디 입력