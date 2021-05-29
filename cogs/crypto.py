from re import X
import discord
from discord.ext import commands, tasks
import aiohttp
from datetime import datetime
import time
from utilsdb import sqlt

ENABLE_CRYPTO = False
MIN_VALUE = 5000000
if ENABLE_CRYPTO:
    with open('API_KEY.txt', 'r') as f:
        API_KEY = f.read()

@tasks.loop(minutes = 1)
async def whaletrans(channel):
    embed = discord.Embed(description = 'Gets data from the [whale alert api](https://whale-alert.io/) and posts it every minute.')
    embed.set_author(name = 'Whale alert', icon_url = 'https://pbs.twimg.com/profile_images/1132579647374417921/9ifIGXEQ_400x400.png')
    embed.set_thumbnail(url = 'https://pbs.twimg.com/profile_images/1132579647374417921/9ifIGXEQ_400x400.png')
    t = int(time.time())
    trn = await sqlt.checktime(channel)
    print(t-trn)
    if trn == None or int(t-trn) >= 3600:
        await sqlt.updatetime(channel, t)
        return
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.whale-alert.io/v1/transactions?api_key={API_KEY}&min_value={MIN_VALUE}&start={int(trn)}') as response:
                dat = await response.json()
                dat['count']
                print(dat['count'])
                if dat['count'] == 0:
                    await sqlt.updatetime(channel, t)
                    return
                else:
                    for i in range(0, dat['count']):
                        embed.clear_fields()
                        trans = dat['transactions'][i]
                        embed.add_field(name = 'Blockchain', value = f'{trans["blockchain"]}', inline = True)
                        embed.add_field(name = 'Coin:', value = f"{trans['symbol']}", inline = True)
                        embed.add_field(name = 'Transaction type:', value = f"{trans['transaction_type']}", inline = True)
                        embed.add_field(name = 'Transaction hash:', value = f"{trans['hash']}", inline = False)
                        embed.add_field(name = f"From (owner type: {trans['from']['owner_type']}):", value = f"{trans['from']['address']}", inline = False)
                        embed.add_field(name = f"To (owner type: {trans['to']['owner_type']}):", value = f"{trans['to']['address']}", inline = False)
                        embed.add_field(name = 'Amount:', value = f"{'{:,}'.format(trans['amount'])} **{trans['symbol']}** / {'{:,}'.format(trans['amount_usd'])} **USD**", inline = False)
                        embed.set_footer(text = f'{datetime.utcfromtimestamp(int(trn)).strftime("%m-%d | %H:%M")}', icon_url = 'https://cdn.discordapp.com/avatars/695608937503916032/811f272fbeb62b75cc420149edc03018.png')
                        await channel.send(embed = embed)
                await sqlt.updatetime(channel, t)

class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def csetup(self, ctx, channel:discord.TextChannel):
        if sqlt.checkcrypto(channel):
            await ctx.send("You can only have 1 channel sending updates.")
        else:
            await sqlt.createcchannel(channel)
            whaletrans.start(channel)
            await ctx.send("Success!")

    @commands.command()
    async def cstop(self, ctx, channel:discord.TextChannel):
        if not await sqlt.checktime(channel):
            await ctx.send("This channel is not sending updates.")
        else:
            await sqlt.removecrypto(channel)
            await ctx.send("Sucessfully stop sending updates.")

def setup(bot):
    bot.add_cog(Crypto(bot))
