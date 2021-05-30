import discord
from discord import file
from discord.ext import commands, tasks
import asyncio
from utilsdb import sqlt
import random
import aiohttp
import time

# Card images from GreysonX on deviantart and Kaiji Ultimate Survivor
#bruhmoment

class Kaiji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    
    @commands.command(aliases = ['er', 'cardrules', 'ecardr', 'erules', 'ecardinfo'])
    async def ecardrules(self, ctx):
        how = """One game has multiple rounds.
        The Emperor side starts off by placing his card down first face down,
        the Slave side has to counter attack with the card of his choice.
        If the Emperor side played a citizen and the Slave side also played a citizen,
        it is a draw, both citizen cards are out of the round and it moves on to the next turn.
        The round finishes when the Emperor side descides to play the emperor card,
        if the Slave side guesses the Emperor side played the emperor then can then counter attack with the slave,
        beating the emperor and winning the round,
        however if they do not guess the Emperor side played the emperor and place a citizen instead they lose the round."""
        
        embed = discord.Embed()
        embed.add_field(name = "Usage:", value = ".duel [opponent] [bet amount]", inline = False)
        embed.add_field(name = "What is Ecard?", value = "Ecard is a PvP card game from the based manga Kaiji.", inline = False)
        embed.set_footer(text = "Made by v999 :)")
        embed.add_field(name= "and?", value = "The Emperor has ultimate power to give money (ie. most powerful card). Citizens cannot disobey him because they want money (i.e. Citizen loses to Emperor). The Slave has nothing to lose and has no use of money, therefore the slave can defeat the Emperor (i.e. The Slave loses to the Citizen card but wins over the Emperor card).", inline = False)
        embed.add_field(name= "What's the setup?", value = "The game is played with one side having four Citizen cards and an Emperor card (Emperor side). The other side having four Citizen cards and a Slave card (Slave side).", inline = False)
        embed.add_field(name= "How does the game go?", value = how, inline = False)
        embed.add_field(name= "How do rounds work?", value = "The Emperor side start the first round, then the Slave side for the second round, they keep switching who starts back and forth until the game is over. Within each round the Emperor and Slave place their cards down first back and forth.", inline = False)
        embed.add_field(name= "How does one win a game?", value = "The game has 8 total rounds. The odds of the Slave side winning for each round is mathematically 1/4. For the Slave side to win a game they need to win a total of 2 rounds. For the Emperor side to win they need to win a total of 6 rounds. Which ever side wins their required amount of rounds first wins the game.", inline = False)
        await ctx.send(embed = embed)

    @commands.command(aliases = ['duel', 'ec'])
    @commands.guild_only()
    async def ecard(self, ctx, user: discord.User, beet):
        currentbalo = await sqlt.checkbal(ctx.guild, ctx.author)
        currentbalopo = await sqlt.checkbal(ctx.guild, user)
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
        slave = 0
        currentpl = 0
        nextpl = 0
        turns = 0
        firstp = 0
        secondp = 0
        kingpoints = 0
        slavepoints = 0
        gamestarted = 0
        roundz = 0
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


                                userx = user #ctx.author user
                                
                                
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
                                try:
                                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                                except asyncio.TimeoutError:
                                    await ctx.author.send("Your opponent didn't accept/decline in time.")
                                    await userx.send("Invitation timed out.")
                                    return
                                brurr = 1
                                if str(reaction.emoji) == '\u2705':
                                    await userx.send('Duel accepted!')

                                    await sqlt.removebal(ctx.guild, userx, float(betf))
                                    await sqlt.removebal(ctx.guild, ctx.author, float(betf))

                                    if betf > balf or betf > balof:
                                        await ctx.author.send("One of you spent money. Ending the duel.")
                                        await ctx.userx("One of you spent money. Ending the duel.")
                                        loop.stop()
                                    
                                    await sqlt.removebal(ctx.guild, ctx.author, betf)
                                    await sqlt.removebal(ctx.guild, userx, betf)

                                    await userx.send(str(betf) + ' MTC has been temporarily removed from your balance for this duel.')

                                    await userx.send(ctx.author.name + ' is picking his preference between Emperor and Slave.')
                                    await ctx.author.send( str(user.name) + ' has accepted your duel request!')

                                    await ctx.author.send(str(betf) + ' MTC has been temporarily removed from your balance for this duel.')

                                    messageca = await ctx.author.send("React with :yellow_square: if you want to play Emperor or with :red_square: if you want to play Slave.")
                                    emojisca = ['\U0001F7E8', '\U0001F7E5']
                                    for emoji in emojisca:
                                        await messageca.add_reaction(emoji)
                                    def check(reaction, user):
                                        return user == ctx.author and str(reaction.emoji) in emojisca
                                    try:
                                        reaction, ctx.author = await self.bot.wait_for('reaction_add', timeout=60, check=check)
                                    except asyncio.TimeoutError:
                                        await ctx.author.send("You took too long to choose.")
                                        await userx.send("Your opponent took too long to choose.")
                                        return
                                    if str(reaction.emoji) == '\U0001F7E8':
                                        await ctx.author.send('You chose Emperor!')
                                        await ctx.author.send('Your opponent is picking whether or not he agrees. If he does not the Slave and Emperor will be randomized.')
                                        message = await userx.send("Your opponent wants to play Emperor :yellow_square:, do you agree with his preference? If not the Emperor will be chosen randomly.")
                                        emojis = ['\u2705', '\u274C']
                                        for emoji in emojis:
                                            await message.add_reaction(emoji)
                                        def check(reaction, user):
                                            return user == userx and str(reaction.emoji) in emojis
                                        try:
                                            reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
                                        except asyncio.TimeoutError:
                                            await ctx.author.send("Your opponent took too long to choose.")
                                            await userx.send("You took too long to choose.")
                                            return

                                        if str(reaction.emoji) == '\u2705':
                                            await userx.send("Your opponent is playing the Emperor. You are playing Slave.")
                                            await ctx.author.send('Your opponent supports your preference, you are playing Emperor!')
                                            plyr1 = 1
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
                                        
                                        try:
                                            reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
                                        except asyncio.TimeoutError:
                                            await ctx.author.send("Your opponent took too long to choose.")
                                            await userx.send("You took too long to choose.")
                                            return


                                        if str(reaction.emoji) == '\u2705':
                                            await userx.send("Your opponent is playing the Slave. You are playing Emperor.")
                                            await ctx.author.send('Your opponent supports your preference, you are playing Slave!')
                                            plyr1 = 2
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
                                        firstp = king
                                        secondp = slave
                                        gamestarted = 1
                                    else:
                                        await ctx.author.send('elsed')
                                        await ctx.author.send(plyr1)
                                        king = userx
                                        slave = ctx.author
                                        firstp = king
                                        secondp = slave
                                        gamestarted = 1
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

        if gamestarted == 1:
            roundz = 1
            kingpoints = 0
            slavepoints = 0

            bluemo = "\U0001F7E6"
            yelmo = "\U0001F7E8"
            redmo = "\U0001F7E5"
            
            emp5 = "https://media.discordapp.net/attachments/847576142290354236/847578461312385054/emp5.jpg"
            emp4 = "https://media.discordapp.net/attachments/847576142290354236/847578459864956969/emp4.jpg"
            emp3 = "https://media.discordapp.net/attachments/847576142290354236/847578431289557022/emp3.jpg"
            emp2 = "https://media.discordapp.net/attachments/847576142290354236/847578429662691338/emp2.jpg"
            emp1 = "https://media.discordapp.net/attachments/847576142290354236/847578422225797150/emp1.jpg"

            slv5 = "https://media.discordapp.net/attachments/847576142290354236/847578464714227732/slave5.jpg"
            slv4 = "https://media.discordapp.net/attachments/847576142290354236/847578462504222750/slave4.jpg"
            slv3 = "https://media.discordapp.net/attachments/847576142290354236/847578460141912064/slave3.jpg"
            slv2 = "https://media.discordapp.net/attachments/847576142290354236/847578457561890836/slave2.jpg"
            slv1 = "https://media.discordapp.net/attachments/847576142290354236/847578433584234586/slave1.jpg"

            cardbak = "https://media.discordapp.net/attachments/847576142290354236/848337794631598090/cardbak.jpg"

            citc = "https://media.discordapp.net/attachments/847576142290354236/847578421399650334/citizen.jpg"


            while (int(kingpoints) < 6 and int(slavepoints) < 2):
                weeznum = int(roundz)

                if (weeznum % 2) == 0:

                    firstp = slave
                    secondp = king

                    fi5 = slv5
                    fi4 = slv4
                    fi3 = slv3
                    fi2 = slv2
                    fi1 = slv1
                    fimo = redmo
                    fine = "Slave"

                    se5 = emp5
                    se4 = emp4
                    se3 = emp3
                    se2 = emp2
                    se1 = emp1
                    semo = yelmo
                    sene = "Emperor"

                else:

                    firstp = king
                    secondp = slave

                    fi5 = emp5
                    fi4 = emp4
                    fi3 = emp3
                    fi2 = emp2
                    fi1 = emp1
                    fimo = yelmo
                    fine = "Emperor"

                    se5 = slv5
                    se4 = slv4
                    se3 = slv3
                    se2 = slv2
                    se1 = slv1
                    semo = redmo
                    sene = "Slave"
                
                turns = 1
                cupd = 0
                nexd = 0

                while (int(turns) < 5):

                    if turns == 1:
                        cupd = fi5
                        nexd = se5
                    elif turns == 2:
                        cupd = fi4
                        nexd = se4
                    elif turns == 3:
                        cupd = fi3
                        nexd = se3
                    elif turns == 4:
                        cupd = fi2
                        nexd = se2
                    elif turns == 5:
                        cupd = fi1
                        nexd = se1
                        

                    currentpl = firstp
                    nextpl  = secondp

                    await nextpl.send("Your opponent is picking a card.")

                    messageca = await currentpl.send(cupd)

                    emojisca = [bluemo, fimo]
                    for emoji in emojisca:
                        await messageca.add_reaction(emoji)
                    def check(reaction, user):
                        return user == currentpl and str(reaction.emoji) in emojisca
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
                    except asyncio.TimeoutError:
                        await nextpl.send("Your opponent took too long to choose. You won " + betf + " MCT!")
                        await currentpl.send("You took too long to choose. You lost " + betf + " MCT.")

                        await sqlt.addbal(ctx.guild, nextpl, float(betf))
                        await sqlt.removebal(ctx.guild, currentpl, float(betf))

                        return

                    if str(reaction.emoji) == fimo:
                        await currentpl.send('You chose '+ fine + "!" )
                        owncardbackmsg = await currentpl.send(cardbak)

                        await messageca.delete()

                        await nextpl.send("Your opponent chose his card, time to pick yours!")
                        cardbackmsg = await nextpl.send(cardbak)

                        


                        
                        messageca = await nextpl.send(nexd)

                        emojisca = [bluemo, semo]
                        for emoji in emojisca:
                            await messageca.add_reaction(emoji)
                        def check(reaction, user):
                            return user == nextpl and str(reaction.emoji) in emojisca
                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
                        except asyncio.TimeoutError:
                            await currentpl.send("Your opponent took too long to choose. You won " + betf + " MCT!")
                            await nextpl.send("You took too long to choose. You lost " + betf + " MCT.")

                            await sqlt.addbal(ctx.guild, currentpl, float(betf))
                            await sqlt.removebal(ctx.guild, nextpl, float(betf))

                            return

                        if str(reaction.emoji) == semo:
                            
                            owncardbackreplymsg = await nextpl.send(cardbak)
                            await nextpl.send('You chose '+ sene + "!" )

                            await messageca.delete()

                            cardbackreplymsg = await currentpl.send(cardbak)
                            await currentpl.send("Your opponent chose his card.")

                            revmsgc = await currentpl.send("Time to reveal the cards...")
                            revmsgn = await nextpl.send("Time to reveal the cards...")
                            await asyncio.sleep(0.4)
                            await revmsgc.edit(content="Time to reveal the cards...3")
                            await revmsgn.edit(content="Time to reveal the cards...3")
                            await asyncio.sleep(0.3)
                            await revmsgc.edit(content="Time to reveal the cards...3...2")
                            await revmsgn.edit(content="Time to reveal the cards...3...2")
                            await asyncio.sleep(0.3)
                            await revmsgc.edit(content="Time to reveal the cards...3...2...1")
                            await revmsgn.edit(content="Time to reveal the cards...3...2...1")
                            await asyncio.sleep(0.3)
                            await revmsgc.delete()
                            await revmsgn.delete()
                            await asyncio.sleep(0.3)

                            await owncardbackmsg.edit(content=fi1)
                            await cardbackmsg.edit(content=fi1)
                            await owncardbackreplymsg.edit(content=se1)
                            await cardbackreplymsg.edit(content=se1)
                            await asyncio.sleep(0.3)

                            slavepoints = int(slavepoints) + 1

                            await king.send("The slave defeats the Emperor! You lost this round!")
                            await king.send("Your opponent just won a point!")

                            await slave.send("The slave defeats the Emperor! You won this round!")
                            await slave.send("You just won a point!")

                            await slave.send("Score: " + str(slavepoints) + "/2 for Slave  " + str(kingpoints) + "/6 for Emperor")
                            await king.send("Score: " + str(slavepoints) + "/2 for Slave  " + str(kingpoints) + "/6 for Emperor")

                            turns = 100
                        

                            


                            

                        else:


                            owncardbackreplymsg = await nextpl.send(cardbak)
                            await nextpl.send("You chose Citizen!")

                            await messageca.delete()

                            cardbackreplymsg = await currentpl.send(cardbak)
                            await currentpl.send("Your opponent chose his card.")

                            revmsgc = await currentpl.send("Time to reveal the cards...")
                            revmsgn = await nextpl.send("Time to reveal the cards...")
                            await asyncio.sleep(0.4)
                            await revmsgc.edit(content="Time to reveal the cards...3")
                            await revmsgn.edit(content="Time to reveal the cards...3")
                            await asyncio.sleep(0.3)
                            await revmsgc.edit(content="Time to reveal the cards...3...2")
                            await revmsgn.edit(content="Time to reveal the cards...3...2")
                            await asyncio.sleep(0.3)
                            await revmsgc.edit(content="Time to reveal the cards...3...2...1")
                            await revmsgn.edit(content="Time to reveal the cards...3...2...1")
                            await asyncio.sleep(0.3)
                            await revmsgc.delete()
                            await revmsgn.delete()
                            await asyncio.sleep(0.3)

                            await owncardbackmsg.edit(content=fi1)
                            await cardbackmsg.edit(content=fi1)
                            await owncardbackreplymsg.edit(content=citc)
                            await cardbackreplymsg.edit(content=citc)
                            await asyncio.sleep(0.3)

                            if currentpl == king:

                                kingpoints = int(kingpoints) + 1

                                await king.send("The Emperor defeats the Citizen! You won this round!")
                                await king.send("You just won a point!")

                                await slave.send("The Emperor defeats the Citizen! You lost this round!")
                                await slave.send("Your opponent just won a point!")

                                await slave.send("Score: " + str(slavepoints) + "/2 for Slave  " + str(kingpoints) + "/6 for Emperor")
                                await king.send("Score: " + str(slavepoints) + "/2 for Slave  " + str(kingpoints) + "/6 for Emperor")

                                turns = 100
                            
                            elif currentpl == slave:
                                
                                kingpoints = int(kingpoints) + 1

                                await king.send("The Citizen defeats the Slave! You won this round!")
                                await king.send("You just won a point!")

                                await slave.send("The Citizen defeats the Slave! You lost this round!")
                                await slave.send("Your opponent just won a point!")

                                await slave.send("Score: " + str(slavepoints) + "/2 for Slave  " + str(kingpoints) + "/6 for Emperor")
                                await king.send("Score: " + str(slavepoints) + "/2 for Slave  " + str(kingpoints) + "/6 for Emperor")

                                turns = 100
                            


                        

                    else:

                        await currentpl.send("You chose Citizen!")
                        owncardbackmsg = await currentpl.send(cardbak)

                        await messageca.delete()

                        await nextpl.send("Your opponent chose his card, time to pick yours!")
                        cardbackmsg = await nextpl.send(cardbak)

                        


                        
                        messageca = await nextpl.send(nexd)

                        emojisca = [bluemo, semo]
                        for emoji in emojisca:
                            await messageca.add_reaction(emoji)
                        def check(reaction, user):
                            return user == nextpl and str(reaction.emoji) in emojisca
                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
                        except asyncio.TimeoutError:
                            await currentpl.send("Your opponent took too long to choose. You won " + betf + " MCT!")
                            await nextpl.send("You took too long to choose. You lost " + betf + " MCT.")

                            await sqlt.addbal(ctx.guild, currentpl, float(betf))
                            await sqlt.removebal(ctx.guild, nextpl, float(betf))

                            return

                        if str(reaction.emoji) == semo:
                            
                            owncardbackreplymsg = await nextpl.send(cardbak)
                            await nextpl.send('You chose '+ sene + "!" )

                            await messageca.delete()

                            cardbackreplymsg = await currentpl.send(cardbak)
                            await currentpl.send("Your opponent chose his card.")

                            revmsgc = await currentpl.send("Time to reveal the cards...")
                            revmsgn = await nextpl.send("Time to reveal the cards...")
                            await asyncio.sleep(0.4)
                            await revmsgc.edit(content="Time to reveal the cards...3")
                            await revmsgn.edit(content="Time to reveal the cards...3")
                            await asyncio.sleep(0.3)
                            await revmsgc.edit(content="Time to reveal the cards...3...2")
                            await revmsgn.edit(content="Time to reveal the cards...3...2")
                            await asyncio.sleep(0.3)
                            await revmsgc.edit(content="Time to reveal the cards...3...2...1")
                            await revmsgn.edit(content="Time to reveal the cards...3...2...1")
                            await asyncio.sleep(0.3)
                            await revmsgc.delete()
                            await revmsgn.delete()
                            await asyncio.sleep(0.3)

                            await owncardbackmsg.edit(content=citc)
                            await cardbackmsg.edit(content=citc)
                            await owncardbackreplymsg.edit(content=se1)
                            await cardbackreplymsg.edit(content=se1)
                            await asyncio.sleep(0.3)

                            if currentpl == king:

                                kingpoints = int(kingpoints) + 1

                                await king.send("The Citizen defeats the Slave! You won this round!")
                                await king.send("You just won a point!")

                                await slave.send("The Citizen defeats the Slave! You lost this round!")
                                await slave.send("Your opponent just won a point!")

                                await slave.send("Score: " + str(slavepoints) + "/2 for Slave  " + str(kingpoints) + "/6 for Emperor")
                                await king.send("Score: " + str(slavepoints) + "/2 for Slave  " + str(kingpoints) + "/6 for Emperor")

                                turns = 100
                            
                            elif currentpl == slave:
                                
                                kingpoints = int(kingpoints) + 1

                                await king.send("The Emperor defeats the Citizen! You won this round!")
                                await king.send("You just won a point!")

                                await slave.send("The Emperor defeats the Citizen! You lost this round!")
                                await slave.send("Your opponent just won a point!")

                                await slave.send("Score: " + str(slavepoints) + "/2 for Slave  " + str(kingpoints) + "/6 for Emperor")
                                await king.send("Score: " + str(slavepoints) + "/2 for Slave  " + str(kingpoints) + "/6 for Emperor")

                                turns = 100
                        

                            


                            

                        else:


                            owncardbackreplymsg = await nextpl.send(cardbak)
                            await nextpl.send("You chose Citizen!")

                            await messageca.delete()

                            cardbackreplymsg = await currentpl.send(cardbak)
                            await currentpl.send("Your opponent chose his card.")

                            revmsgc = await currentpl.send("Time to reveal the cards...")
                            revmsgn = await nextpl.send("Time to reveal the cards...")
                            await asyncio.sleep(0.4)
                            await revmsgc.edit(content="Time to reveal the cards...3")
                            await revmsgn.edit(content="Time to reveal the cards...3")
                            await asyncio.sleep(0.3)
                            await revmsgc.edit(content="Time to reveal the cards...3...2")
                            await revmsgn.edit(content="Time to reveal the cards...3...2")
                            await asyncio.sleep(0.3)
                            await revmsgc.edit(content="Time to reveal the cards...3...2...1")
                            await revmsgn.edit(content="Time to reveal the cards...3...2...1")
                            await asyncio.sleep(0.3)
                            await revmsgc.delete()
                            await revmsgn.delete()
                            await asyncio.sleep(0.3)

                            await owncardbackmsg.edit(content=citc)
                            await cardbackmsg.edit(content=citc)
                            await owncardbackreplymsg.edit(content=citc)
                            await cardbackreplymsg.edit(content=citc)
                            await asyncio.sleep(0.3)



                            await king.send("The citizens defeat each other! It's a tie!")
                            await king.send("Moving on to the next turn...")

                            await slave.send("The citizens defeat each other! It's a tie!")
                            await slave.send("Moving on to the next turn...")

                            await slave.send("Score: " + str(slavepoints) + "/2 for Slave  " + str(kingpoints) + "/6 for Emperor")
                            await king.send("Score: " + str(slavepoints) + "/2 for Slave  " + str(kingpoints) + "/6 for Emperor")

                            turns = int(turns) + 1
                            

                if turns == 5:

                    await king.send("You only have an Emperor left! You lost!")
                    await king.send("Your opponent just got a point!")

                    await slave.send("Your opponent only has an Emperor left! You won!")
                    await slave.send("You just got a point!")

                    await slave.send("Score: " + str(slavepoints) + "/2 for Slave  " + str(kingpoints) + "/6 for Emperor")
                    await king.send("Score: " + str(slavepoints) + "/2 for Slave  " + str(kingpoints) + "/6 for Emperor")
            

            if kingpoints == 6:

                if king == ctx.author:
                
                    await king.send("The game has ended! You won " + str(betf) + " MCT")
                    await slave.send("The game has ended! " + str(ctx.author.name) + " has won " + str(betf) + " MCT. Too bad...")
                
                elif king == userx:
                    
                    await king.send("The game has ended! You won " + str(betf) + " MCT")
                    await slave.send("The game has ended! " + str(userx.name) + " has won " + str(betf) + " MCT. Too bad...")



            elif slavepoints == 2:

                if king == ctx.author:
                
                    await slave.send("The game has ended! You won " + str(betf) + " MCT")
                    await king.send("The game has ended! " + str(ctx.author.name) + " has won " + str(betf) + " MCT. Too bad...")

                    await sqlt.addbal(ctx.guild, ctx.author, betf)
                
                elif king == userx:
                    
                    await slave.send("The game has ended! You won " + str(betf) + " MCT")
                    await king.send("The game has ended! " + str(userx.name) + " has won " + str(betf) + " MCT. Too bad...")

                    await sqlt.addbal(ctx.guild, userx, betf)




def setup(bot):
    bot.add_cog(Kaiji(bot))
