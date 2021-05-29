import discord
from discord.ext import commands
import aiohttp
from utilsdb import sqlt

class Gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rnd(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.random.org/integers/?num=1&min=1&max=200&col=1&base=10&format=plain&rnd=new') as response:
                result = await response.text()
        await ctx.send(result)

    @commands.command(aliases = ['cf', 'flip'])
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def coinflip(self, ctx, v, m):
        bank = await sqlt.getbankval(ctx.guild)
        currentbal = await sqlt.checkbal(ctx.guild, ctx.author)
        if v.lower() == 'all':
            v = currentbal
        t = float(v)
        val = round(t, 2)
        if val > currentbal:
            await ctx.send("You don't have enough MCT")
        elif val > bank:
            await ctx.send("The bank doesn't have enough money.")
        else:
            if val < 0.01:
                await ctx.send("Please enter a minimum amount of 0.01")
                return
            async with aiohttp.ClientSession() as session:
                async with session.get('https://www.random.org/integers/?num=1&min=1&max=200&col=1&base=10&format=plain&rnd=new') as response:
                    r = await response.text()
            if m.lower().startswith('b'):
                if int(r) >= 102:
                    await ctx.send('https://cdn.discordapp.com/attachments/695949677694156834/847557850598211634/blueg.gif')
                    await sqlt.removebank(ctx.guild, val)
                    await sqlt.addbal(ctx.guild, ctx.author, val)
                elif int(r) == 100 or int(r) == 101:
                    await ctx.send('GET GREENED ON')
                    await sqlt.addbank(ctx.guild, val)
                    await sqlt.removebal(ctx.guild, ctx.author, val)
                else:
                    await ctx.send('https://cdn.discordapp.com/attachments/695949677694156834/847557856944717834/redg.gif')
                    await sqlt.addbank(ctx.guild, val)
                    await sqlt.removebal(ctx.guild, ctx.author, val)
            elif m.lower().startswith('r'):
                if int(r) <= 99:
                    await ctx.send('https://cdn.discordapp.com/attachments/695949677694156834/847557856944717834/redg.gif')
                    await sqlt.removebank(ctx.guild, val)
                    await sqlt.addbal(ctx.guild, ctx.author, val)
                elif int(r) == 100 or int(r) == 101:
                    await ctx.send('GET GREENED ON')
                    await sqlt.addbank(ctx.guild, val)
                    await sqlt.removebal(ctx.guild, ctx.author, val)
                else:
                    await ctx.send('https://cdn.discordapp.com/attachments/695949677694156834/847557850598211634/blueg.gif')
                    await sqlt.addbank(ctx.guild, val)
                    await sqlt.removebal(ctx.guild, ctx.author, val)
            else:
                await ctx.send("Please enter a valid bet choice. *Red / Blue*")
            print(await sqlt.getbankval(ctx.guild))

def setup(bot):
    bot.add_cog(Gamble(bot))