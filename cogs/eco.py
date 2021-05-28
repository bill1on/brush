import discord
from discord import file
from discord.ext import commands, tasks
import asyncio
from utilsdb import sqlt
from datetime import datetime
import random
import aiohttp

class Eco(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bal(self, ctx):
        tbal = await sqlt.checkbal(ctx.author)
        pbal = round(tbal, 2)
        if not isinstance(pbal, bool):
            pos = await sqlt.balleader(ctx.author)
            if str(pos).endswith('1'):
                rank = str(pos) + 'st'
            elif str(pos).endswith('2'):
                rank = str(pos) + 'nd'
            elif str(pos).endswith('3'):
                rank = str(pos) + 'rd'
            else:
                rank = str(pos) + 'th'
            embed = discord.Embed()
            embed.set_author(name = f"{ctx.author.name + '#' + ctx.author.discriminator}", icon_url = f'{ctx.author.avatar_url}')
            embed.add_field(name = '**Leaderboard**', value = f"You are **{rank}** on the leaderboard!")
            embed.add_field(name = '**Balance**', value = f'\n<:mdct:843999368095989770> **{pbal}** MCT', inline = False)
            now = datetime.now()
            embed.set_footer(text = f"{str(now.day) + '/' + str(now.month) + '  ' + str(now.hour) + ':' + str(now.minute)}", icon_url = 'https://media.discordapp.net/attachments/756537548180029481/846092160193396757/images.png')
            await ctx.send(embed = embed)
        else:
            await sqlt.createbal(ctx.author)
            pbal = await sqlt.checkbal(ctx.author)
            pos = await sqlt.balleader(ctx.author)
            if str(pos).endswith('1'):
                rank = str(pos) + 'st'
            elif str(pos).endswith('2'):
                rank = str(pos) + 'nd'
            elif str(pos).endswith('3'):
                rank = str(pos) + 'rd'
            else:
                rank = str(pos) + 'th'
            embed = discord.Embed()
            embed.set_author(name = f"{ctx.author.name + '#' + ctx.author.discriminator}", icon_url = f'{ctx.author.avatar_url}')
            embed.add_field(name = '**Leaderboard**', value = f"You are **{rank}** on the leaderboard!")
            embed.add_field(name = '**Balance**', value = f'\n<:mdct:843999368095989770> **{pbal}** MCT', inline = False)
            now = datetime.now()
            embed.set_footer(text = f"{str(now.day) + '/' + str(now.month) + '  ' + str(now.hour) + ':' + str(now.minute)}", icon_url = 'https://media.discordapp.net/attachments/756537548180029481/846092160193396757/images.png')
            await ctx.send(embed = embed)

    @commands.command()
    async def rnd(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.random.org/integers/?num=1&min=1&max=100&col=1&base=10&format=plain&rnd=new') as response:
                result = await response.text()
        await ctx.send(result)

    @commands.command(aliases = ['cf', 'flip'])
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def coinflip(self, ctx, v, m):
        bank = await sqlt.getbankval()
        currentbal = await sqlt.checkbal(ctx.author)
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
                    await sqlt.removebank(val)
                    await sqlt.addbal(ctx.author, val)
                elif int(r) == 100 or int(r) == 101:
                    await ctx.send('GET GREENED ON')
                    await sqlt.addbank(val)
                    await sqlt.removebal(ctx.author, val)
                else:
                    await ctx.send('https://cdn.discordapp.com/attachments/695949677694156834/847557856944717834/redg.gif')
                    await sqlt.addbank(val)
                    await sqlt.removebal(ctx.author, val)
            elif m.lower().startswith('r'):
                if int(r) <= 99:
                    await ctx.send('https://cdn.discordapp.com/attachments/695949677694156834/847557856944717834/redg.gif')
                    await sqlt.removebank(val)
                    await sqlt.addbal(ctx.author, val)
                elif int(r) == 100 or int(r) == 101:
                    await ctx.send('GET GREENED ON')
                    await sqlt.addbank(val)
                    await sqlt.removebal(ctx.author, val)
                else:
                    await ctx.send('https://cdn.discordapp.com/attachments/695949677694156834/847557850598211634/blueg.gif')
                    await sqlt.addbank(val)
                    await sqlt.removebal(ctx.author, val)
            else:
                await ctx.send("Please enter a valid bet choice. *Red / Blue*")
            print(await sqlt.getbankval())

    @commands.command()
    async def bank(self, ctx):
        now = datetime.now()
        embed = discord.Embed()
        embed.set_author(name = f"{ctx.author.name + '#' + ctx.author.discriminator}", icon_url = f'{ctx.author.avatar_url}')
        embed.add_field(name = '**Bank**', value = f"The bank has : <:mdct:843999368095989770> {round(await sqlt.getbankval(), 2)} MCT")
        embed.set_footer(text = f"{str(now.day) + '/' + str(now.month) + '  ' + str(now.hour) + ':' + str(now.minute)}", icon_url = 'https://media.discordapp.net/attachments/756537548180029481/846092160193396757/images.png')
        await ctx.send(embed = embed)

    @commands.command(aliases = ['lb', 'baltop'])
    async def leaderboard(self, ctx):
        txt = ''
        cnt = 1
        ind = ''
        now = datetime.now()
        embed = discord.Embed()
        embed.set_author(name = f"{ctx.author.name + '#' + ctx.author.discriminator}", icon_url = f'{ctx.author.avatar_url}')
        embed.set_footer(text = f"{str(now.day) + '/' + str(now.month) + '  ' + str(now.hour) + ':' + str(now.minute)}", icon_url = 'https://media.discordapp.net/attachments/756537548180029481/846092160193396757/images.png')
        lead = await sqlt.lead()
        for i in lead:
            if cnt == 1:
                mbm = await ctx.guild.fetch_member(i[0])
                role = ctx.guild.get_role(768927936535068692)
                await mbm.add_roles(role)
                ind = str(cnt) + 'st'
            elif str(cnt).endswith('1'):
                ind = str(cnt) + 'st'
            elif str(cnt).endswith('2'):
                ind = str(cnt) + 'nd'
            elif str(cnt).endswith('3'):
                ind = str(cnt) + 'rd'
            else:
                ind = str(cnt) + 'th'
            mbm = await ctx.guild.fetch_member(i[0])
            bal = await sqlt.checkbal(mbm)
            txt = txt + f'**{ind}**. {mbm.name}#{mbm.discriminator} | <:mdct:843999368095989770> **{round(bal, 2)}** MCT\n'
            cnt += 1
        embed.add_field(name = '**Leaderboard.**', value = txt)
        await ctx.send(embed=embed)

    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed(description = "**__Rules:__**\n-Scamming | refund for buyer and ban from using bot for seller\n-Maximum 2 listings per person\n**__Usage:__**\n`.buy *name of item*` | `.sell *name* *value* *description*`\n\n**SHOP:**", color = 1048464)
        embed.set_author(name = 'Midnight Crew Shop', icon_url = 'https://cdn.discordapp.com/emojis/846067291589574666.png')
        embed.set_thumbnail(url = "https://media.discordapp.net/attachments/836912159573147649/847872413081141308/rffcgddd.png?width=504&height=640")
        if not await sqlt.checkshop(ctx.guild):
            embed.add_field(name = "Oops!", value = "Seems like there's nothing in the shop! <:sadge:836984964729274410>")
        else:
            shoplisting = await sqlt.getshop(ctx.guild)
            print(shoplisting)
            for i in shoplisting:
                member = ctx.guild.get_member(i[0])
                embed.add_field(name = f"{i[1]} for <:mdct:843999368095989770> **{i[3]}** MCT", value = f"{i[2]}\nSeller: __{member.name}#{member.discriminator}__", inline= False)
        await ctx.send(embed=embed)

    @commands.command()
    async def sell(self, ctx, name, price, *value):
        price = round(float(price), 2)
        if not isinstance(await sqlt.checkbal(ctx.author), bool):
            if await sqlt.listingpermember(ctx.author) >= 2:
                await ctx.send("Can't list more than 2 items!")
            else:
                value = ' '.join(value)
                if len(name) > 20:
                    await ctx.send("Overexceeded 20 characters for name")
                elif len(value) > 50:
                    await ctx.send("Overexceeded 50 characters for value")
                elif float(price) < 0.01:
                    await ctx.send("Invalid price (minimum 0.01)")
                else:
                    slist = await sqlt.checkshopname(name)
                    for i in slist:
                        if name in i:
                            await ctx.send("Name is already used!")
                            return
                    await sqlt.auctionshop(ctx.author, ctx.guild, name, value, price)
                    await ctx.send(f"Sucessfully added {name} to shop for <:mdct:843999368095989770> **{price}** MCT")
        else:
            await ctx.send("You haven't joined yet! Please use .join to start participating!")

    @commands.command()
    async def buy(self, ctx, name):
        items = await sqlt.checkshopname(name)
        if items[0][4] > await sqlt.checkbal(ctx.author):
            await ctx.send("Not enough money")
            return
        elif items[0][0] == ctx.author.id:
            await ctx.send("Can't buy your own product.")
            return
        items = items[0]
        await sqlt.removebal(ctx.author, float(items[4]))
        await ctx.send(f"Sucessfully bought {name} for <:mdct:843999368095989770> **{items[4]}** MCT")
        seller = ctx.guild.get_member(items[0])
        await sqlt.addbal(seller, float(items[4]))
        await seller.send(f"Someone has bought {name}! You've received <:mdct:843999368095989770> **{items[4]}** MCT")
        await sqlt.removeshop(items)

    @commands.command()
    async def remove(self, ctx, name):
        items = await sqlt.checkshopname(name)
        if ctx.author.id == items[0][0]:
            await sqlt.removeshop(items[0])
        else:
            if ctx.author.guild_permissions.administrator:
                await sqlt.removeshop(items[0])
            else:
                await ctx.send("You don't have permissions to remove someone else's item.")

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tip(self, ctx, member:discord.Member, am):
        if int(am) < 0.01:
            await ctx.send("Please enter a valid amount (0.01 minimum)")
        else:
            await sqlt.addbal(member, float(am))
            await sqlt.removebal(ctx.author, float(am))
            await ctx.send(f"Sent <:mdct:843999368095989770> **{am}** MCT to {member}")

def setup(bot):
    bot.add_cog(Eco(bot))
