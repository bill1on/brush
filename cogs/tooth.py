import discord
from discord.ext import commands, tasks
from utilsdb import sqlt
from datetime import datetime, timedelta
import asyncio
import time

class Tooth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg): # an on_message event listener
        if not msg.author.bot:
            if not isinstance(msg.channel, discord.channel.DMChannel): # if the message is not in dms
                if msg.channel.name == 'brush': # and the channel name is brush
                    await asyncio.sleep(0.1)
                    await msg.delete() # delete the message after 0.1 seconds

    @tasks.loop(hours=24) # A loop that loops every 24 hours
    async def lockt(self, user, server):
        if await sqlt.checkb(server, user): # checkb checks whether a person has brushed their teeth
            await sqlt.makef(server, user) #if they have, i will turn to false and a new day will start
        else:
            brole = server.get_role(845716619992105001)
            roles = user.roles # list of roles
            rolelist = "" # role list
            for i in roles:
                if not i.position == 0:
                    rolelist = rolelist + str(i.id) +  ', '  # gets id for each role and makes it into a string
            if not await sqlt.checkrole(server, user):
                await sqlt.roleadd(server, user, rolelist) # adds them to the database
            for role in roles:
                if not role.position == 0:
                    await user.remove_roles(role)
            print(f"Added {brole.name} to {user.name}")
            await user.add_roles(brole) # if the person hasn't brushed their teeth they will get the role (not seeing anything)
            try:
                await user.edit(deafen = True, mute = True)
            except:
                print('User is not in VC')

    @lockt.before_loop
    async def before_lockt(self): # function that is executed before the loop
        hour = 6
        minute = 00
        await self.bot.wait_until_ready()
        now = datetime.now() # current date
        future = datetime(now.year, now.month, now.day, hour, minute) # the future date (using hour and minute which we have given)
        if now.hour == hour: # if the current hour is the same as the hour in the future
            if now.minute > minute: # we will check whether the current minute is higher than the future minute
                future += timedelta(days=1) # if it is, it means that we already surpassed the deadline and it will be moved to the next day
        elif now.hour > hour:
            future += timedelta(days=1) # if the current hour is bigger than the future than we're also ahead and we do the same
        print((future-now).seconds)
        await asyncio.sleep((future-now).seconds) # we then sleep for the time between the current day and the deadline

    @commands.command()
    @commands.guild_only()
    async def brush(self, ctx):
        if await sqlt.checkt(ctx.guild, ctx.author): # checks whether a user is in the database
            if not await sqlt.checkb(ctx.guild, ctx.author): # checks whether the user has brushed their teeth today already
                await sqlt.maket(ctx.guild, ctx.author) # we then turn it to true because they said they did brush their teeth now
                await ctx.send('You brushed your teeth, nice job!')
                roles = await sqlt.roleget(ctx.guild, ctx.author) # gets original roles from db
                if roles == None:
                    await sqlt.addbal(ctx.guild, ctx.author, 1)
                else:
                    rolelist = roles.split(', ')
                    for i in rolelist:
                        if not i == '':
                            role = ctx.guild.get_role(int(i))
                            await ctx.author.add_roles(role) # gives back original roles
                    brole = ctx.guild.get_role(845716619992105001)
                    await ctx.author.remove_roles(brole) # removes b role
                    await sqlt.deleterole(ctx.guild, ctx.author)
                    try:
                        await ctx.author.edit(deafen = False, mute = False)
                    except:
                        print("Couldn't undeafen/unmute user.")
                    await sqlt.addbal(ctx.guild, ctx.author, 1)
        
        else: # if not in database this is sent
            embed = discord.Embed()
            embed.add_field(name = "Want to get started?", value = "Just use .join to start getting reminded!", inline = False)
            embed.set_footer(text = "Made by billion")
            embed.add_field(name= "Already joined but this message still shows up?", value = "Please ping a staff member to help you out.", inline = False)
            await ctx.send(embed = embed)

    @commands.command()
    @commands.guild_only()
    async def join(self, ctx): #join function for joining the database
        fp = open(file= "./files/xqcmald.gif", mode= "rb")
        xqc = discord.File(fp)
        if await sqlt.checkt(ctx.guild, ctx.author): #checks whether a user is already registered
            await ctx.send("YOU ALREADY REGISTERED", file=xqc)
        else:
            await sqlt.addt(ctx.guild, ctx.author) #if the user isnt already in the database they get added to it
            embed = discord.Embed()
            embed.add_field(name = "Success! ✅", value = "\n\nYou have sucessfully joined.\n\nYou will be asked to brush your teeth once every 24 hours.\n\nWant to change this? You can't do this yet. (maybe soon)")
            embed.set_footer(text= "You joined! Nice")
            await ctx.send(embed=embed)
            self.lockt.start(ctx.author, ctx.guild) #the task starts running

def setup(bot):
    bot.add_cog(Tooth(bot))
