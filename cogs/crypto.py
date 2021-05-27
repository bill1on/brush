import discord
from discord.ext import commands, tasks
import aiohttp
import time
from utilsdb import sqlt

@tasks.loop(minutes = 1)
async def whaletrans(channel):
    t = int(time.time())
    trn = await sqlt.checktime(channel)
    if trn == None or int(t-trn) >= 3600:
        await sqlt.updatetime(channel, t)
        return
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.whale-alert.io/v1/transactions?api_key=tuIT4Ag3o0Rd2BSMPZvYB5ByXlaIZzL2&min_value=500000&start={round(trn, 0)}') as response:
                await channel.send(await response.text())

class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def csetup(self, ctx, channel:discord.TextChannel):
        await sqlt.createcchannel(channel)
        whaletrans.start(channel)

def setup(bot):
    bot.add_cog(Crypto(bot))
