import discord
from discord import file
from discord.ext import commands, tasks
import asyncio
from utilsdb import sqlt
import random
import aiohttp
import time

# Card images from GreysonX on deviantart and Kaiji Ultimate Survivor

class Kaiji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['er', 'cardrules', 'ecardr', 'erules', 'ecardinfo'])
    async def ecardrules(self, ctx):
        embed = discord.Embed()
        embed.add_field(name = "Usage:", value = ".duel [opponent] [bet amount]", inline = False)
        embed.add_field(name = "What is Ecard?", value = "Ecard is a PvP card game from the based manga Kaiji.", inline = False)
        embed.set_footer(text = "Made by v999 :)")
        embed.add_field(name= "and?", value = "The Emperor has ultimate power to give money (ie. most powerful card). Citizens cannot disobey him because they want money (i.e. Citizen loses to Emperor). The Slave has nothing to lose and has no use of money, therefore the slave can defeat the Emperor (i.e. The Slave loses to the Citizen card but wins over the Emperor card).", inline = False)
        embed.add_field(name= "What's the setup?", value = "The game is played with one side having four Citizen cards and an Emperor card (Emperor side). The other side having four Citizen cards and a Slave card (Slave side).", inline = False)
        embed.add_field(name= "How does the game go?", value = "One game has multiple rounds. The Emperor side starts off by placing his card down first face down, the Slave side has to counter attack with the card of his choice. If the Emperor side played a citizen and the Slave side also played a citizen, it is a draw, both citizen cards are out of the round and it moves on to the next turn. The round finishes when the Emperor side descides to play the emperor card, if the Slave side guesses the Emperor side played the emperor then can then counter attack with the slave, beating the emperor and winning the round, however if they do not guess the Emperor side played the emperor and place a citizen instead they lose the round.", inline = False)
        embed.add_field(name= "How do rounds work?", value = "The Emperor side start the first round, then the Slave side for the second round, they keep switching who starts back and forth until the game is over. Within each round the Emperor and Slave place their cards down first back and forth.", inline = False)
        embed.add_field(name= "How does one win a game?", value = "The game has 8 total rounds. The odds of the Slave side winning for each round is mathematically 1/4. For the Slave side to win a game they need to win a total of 2 rounds. For the Emperor side to win they need to win a total of 8 rounds. Which ever side wins their required amount of rounds first wins the game.", inline = False)
        await ctx.send(embed = embed)


    @commands.command(aliases = ['duel', 'ec'])
    @commands.guild_only()
    async def ecard(self, ctx, user: discord.User, beet):
        currentbalo = await sqlt.checkbal(ctx.author)
        currentbalopo = await sqlt.checkbal(user)
        tee = float(currentbalo)
        teeop = float(currentbalopo)
        balo = round(tee, 2)
        balop = round(teeop, 2)
        betm = float(beet)
        betr = round(betm, 2)
        betf = float(betr)
        balf = float(balo)
        balof = float(balop)
        plyr1 = 1
        king = 0
        if betf < 0.01:
            await ctx.send("Please enter a minimum amount of 0.01 MCT")
        else:
            if await sqlt.checkt(ctx.guild, ctx.author): #checks whether a user is already registered
                if await sqlt.checkt(ctx.guild, user):
                    if betf > balf:
                        await ctx.send("You do not have enough MCT.")
                    else:
                        if betf > balof:
                            await ctx.send("Your oponent doesn't have enough money.")
                        else:
                            if ctx.author==user:
                                await ctx.send("You can't duel yourself!")
                            else:
                                userx = ctx.author
                                await userx.send(ctx.author.name + " just challenged you to a duel of Ecard for " + str(betr) + " MCT.")
                                await userx.send("You have 60 seconds to accept.")
                                await userx.send("For more information about Ecard do `.erules`")
                                await ctx.send("<@" + str(user.id) + "> " + ctx.author.name + " is challenging you, check direct messages!")

                                message = await userx.send("React with :white_check_mark: to accept or with :x: to decline.")
                                emojis = ['\u2705', '\u274C']
                                for emoji in emojis:
                                    await message.add_reaction(emoji)
                                def check(reaction, user):
                                    return user == userx and str(reaction.emoji) in emojis
#                                try:
                                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                                brurr = 1
                                if str(reaction.emoji) == '\u2705':
                                    await userx.send('Duel accepted!')
                                    await userx.send(ctx.author.name + ' is picking his preference between Emperor and Slave.')
                                    await ctx.author.send( str(user.name) + ' has accepted your duel request!')

                                    messageca = await ctx.author.send("React with :yellow_square: if you want to play Emperor or with :red_square: if you want to play Slave.")
                                    emojisca = ['\U0001F7E8', '\U0001F7E5']
                                    for emoji in emojisca:
                                        await messageca.add_reaction(emoji)
                                    def check(reaction, user):
                                        return user == userx and str(reaction.emoji) in emojisca
                                    reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)

                                    if str(reaction.emoji) == '\U0001F7E8':
                                        await ctx.author.send('You chose Emperor!')
                                        await ctx.author.send('Your opponent is picking whether or not he agrees. If he does not the Slave and Emperor will be randomized.')
                                        message = await userx.send("Your opponent wants to play Emperor :yellow_square:, do you agree with his preference? If not the Emperor will be chosen randomly.")
                                        emojis = ['\u2705', '\u274C']
                                        for emoji in emojis:
                                            await message.add_reaction(emoji)
                                        def check(reaction, user):
                                            return user == userx and str(reaction.emoji) in emojis
                                        reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)

                                        if str(reaction.emoji) == '\u2705':
                                            await userx.send("Your opponent is playing the Emperor.")
                                            await ctx.author.send('Your opponent supports your preference, you are playing Emperor!')
                                        else:
                                            await userx.send("The roles are being randomized...")
                                            await ctx.author.send("Your opponent contested your choice. The roles are being randomized...")
                                            rood = random.SystemRandom()
                                            selu = "12"
                                            plyrdet = (rood.choice(selu))
                                            plyr1 = float(plyrdet)


                                    else:
                                        await ctx.author.send('You chose Slave!')
                                        await ctx.author.send('Your opponent is picking whether or not he agrees. If he does not the Slave and Emperor will be randomized.')
                                        message = await userx.send("Your opponent wants to play Slave :red_square:, do you agree with his preference? If not the Slave will be chosen randomly.")
                                        emojis = ['\u2705', '\u274C']
                                        for emoji in emojis:
                                            await message.add_reaction(emoji)
                                        def check(reaction, user):
                                            return user == userx and str(reaction.emoji) in emojis
                                        reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)

                                        if str(reaction.emoji) == '\u2705':
                                            await userx.send("Your opponent is playing the Slave.")
                                            await ctx.author.send('Your opponent supports your preference, you are playing Slave!')
                                        else:
                                            await userx.send("The roles are being randomized...")
                                            await ctx.author.send("Your opponent contested your choice. The roles are being randomized...")
                                            rood = random.SystemRandom()
                                            selu = "12"
                                            plyrdet = (rood.choice(selu))
                                            plyr1 = float(plyrdet)


                                    if plyr1 == 1:
                                        await ctx.author.send('iffed')
                                        await ctx.author.send(plyr1)
                                        king = ctx.author
                                        slave = userx
                                    else:
                                        await ctx.author.send('elsed')
                                        await ctx.author.send(plyr1)
                                        king = userx
                                        slave = ctx.author

                                    await king.send('Here is your deck. Use :blue_square: for Citizen and :yellow_square: for Emperor.')
                                    messageca = await ctx.author.send("https://cdn.discordapp.com/attachments/847576142290354236/847578461312385054/emp5.jpg")
                                    emojisca = ['\U0001F7E6', '\U0001F7E8']
                                    for emoji in emojisca:
                                        await messageca.add_reaction(emoji)
                                    def check(reaction, user):
                                        return user == userx and str(reaction.emoji) in emojisca
                                    reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)

                                    if str(reaction.emoji) == '\U0001F7E8':
                                        await ctx.author.send('You chose Emperor!')
                                    else:
                                        await ctx.author.send('You chose Citizen!')

                                else:
                                    await ctx.author.send("The Ecard duel with " + userx.name + " was declined.")
                                    await userx.send("Declined.")
                                # there's only two reactions, so if the above function didn't return, it means the second reaction (nay) was used instead
#                                except:
#                                    await userx.send("Automatically Declined / Timed out")
#                                    await ctx.author.send("The Ecard duel with " + userx.name + " was automatically declined or timed out.")
#                                else:
#                                    await ctx.author.send("lole")

                else:
                    await ctx.send("Please enter the @ of a valid opponent.")
            else:
                await ctx.send("You are not registered to the brush bot, do .join to register.")




def setup(bot):
    bot.add_cog(Kaiji(bot))
