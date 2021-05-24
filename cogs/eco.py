import discord
from discord.ext import commands, tasks
import asyncio
from utils import sqlt
from datetime import datetime



class Eco(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bal(self, ctx):
        pbal = await sqlt.checkbal(ctx.author)
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
            # await ctx.send(f"You have : {pbal} MDCT <:mdct:843999368095989770>")
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

def setup(bot):
    bot.add_cog(Eco(bot))