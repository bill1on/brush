import aiosqlite
import discord
from discord.ext import commands, tasks
import aioschedule
from datetime import datetime, timedelta
import asyncio
from cogs import tooth

sqldb = """CREATE TABLE IF NOT EXISTS ACTIVE (
            memberID integer PRIMARY KEY,
            guildID ,
            brushedt int
        )"""

sqlr = """CREATE TABLE IF NOT EXISTS ROLES (
            memberID integer PRIMARY KEY,
            guildID,
            rolelist TEXT
        )"""

sqlb = """CREATE TABLE IF NOT EXISTS BALANCE (
            memberID integer PRIMARY KEY,
            balance float
)"""

sqlg = """CREATE TABLE IF NOT EXISTS BANK (
            balance float
)"""

sqlt = """CREATE TABLE IF NOT EXISTS CRYPTO (
            channelid integer,
            guildid integer,
            time integer
)"""

async def maket(guild, member): #updates the boolean value "brushed" to True of the given user 'member'
    async with aiosqlite.connect('db.db') as db:
        await db.execute(sqldb)
        async with db.cursor() as crs:
            await crs.execute("""SELECT memberID, guildID, brushedt FROM ACTIVE""")
            vals = await crs.fetchall()
            for i in vals:
                if member.id == i[0] and guild.id == i[1]:
                    val = 1
                    await crs.execute(f"""UPDATE ACTIVE SET brushedt = {val} WHERE memberID = {i[0]}""")
                    await db.commit()
                    break

async def loopsql(bot): #loop which is run everytime the bot starts to make sure that the users in the database are running the task
    async with aiosqlite.connect('db.db') as db:
        await db.execute(sqldb)
        async with db.cursor() as crs:
            await crs.execute("""SELECT memberID, guildID FROM ACTIVE""")
            vals = await crs.fetchall()
            for i in vals:
                server = bot.get_guild(int(i[1]))
                member = server.get_member(i[0])
                tooth.Tooth(bot).lockt.start(member, server)

async def makef(guild, member): #makes the boolean value 'brushed' False in the database
    async with aiosqlite.connect('db.db') as db:
        await db.execute(sqldb)
        async with db.cursor() as crs:
            await crs.execute("""SELECT memberID, guildID, brushedt FROM ACTIVE""")
            vals = await crs.fetchall()
            for i in vals:
                if member.id == i[0] and guild.id == i[1]:
                    val = 0
                    await crs.execute(f"""UPDATE ACTIVE SET brushedt = {val} WHERE memberID = {i[0]}""")
                    await db.commit()
                    break

async def checkb(guild, member): #checks whether the boolean value "brushed" is True or False
    async with aiosqlite.connect('db.db') as db:
        await db.execute(sqldb)
        async with db.cursor() as crs:
            await crs.execute("""SELECT memberID, guildID, brushedt FROM ACTIVE""")
            vals = await crs.fetchall()
            for i in vals:
                if member.id == i[0] and guild.id == i[1]:
                    if i[2] == 0:
                        return False
                    elif i[2] == 1:
                        return True

async def checkt(guild, member): # checks whether a person is in the database
    async with aiosqlite.connect('db.db') as db:
        await db.execute(sqldb)
        async with db.cursor() as crs:
            await crs.execute("""SELECT memberID, guildID FROM ACTIVE""")
            vals = await crs.fetchall()  
            for i in vals:
                if member.id == i[0]:
                    if i[1] == guild.id:
                        return True
        return False           
 
async def addt(guild, member): #adds the person to the database
    async with aiosqlite.connect('db.db') as db:
        await db.execute(sqldb)
        async with db.cursor() as crs:
            await crs.execute("""INSERT INTO ACTIVE (guildID, memberID, brushedt) VALUES (:guildID, :memberID, :brushedval)""", {'guildID': guild.id, 'memberID': member.id, 'brushedval': False})
            await db.commit()

async def roleadd(guild, member, rlist): #adds the list of roles to the database that the user currently has
    async with aiosqlite.connect('db.db') as db:
        await db.execute(sqlr)
        async with db.cursor() as crs:
            await crs.execute("""INSERT INTO ROLES (guildID, memberID, rolelist) VALUES (:guildID, :memberID, :roleval)""", {'guildID': guild.id, 'memberID': member.id, 'roleval': rlist})
            await db.commit()

async def roleget(guild, member): # fetches the roles from the database
    async with aiosqlite.connect('db.db') as db:
        await db.execute(sqlr)
        async with db.cursor() as crs:
            await crs.execute("""SELECT memberID, guildID, rolelist FROM ROLES""")
            vals = await crs.fetchall()
            for i in vals:
                if member.id == i[0] and guild.id == i[1]:
                    return i[2]

async def checkrole(guild, member): # checks if the user is in the roles database
    async with aiosqlite.connect('db.db') as db:
        await db.execute(sqlr)
        async with db.cursor() as crs:
            await crs.execute("""SELECT memberID, guildID, rolelist FROM ROLES""")
            vals = await crs.fetchall()
            for i in vals:
                if member.id == i[0] and guild.id == i[1]:
                    return True
                else:
                    return False

async def deleterole(guild, member): # deletes data from user from database
    async with aiosqlite.connect('db.db') as db:
        await db.execute(sqlr)
        async with db.cursor() as crs:
            await crs.execute("""SELECT memberID, guildID FROM ROLES""")
            vals = await crs.fetchall()
            for i in vals:
                if member.id == i[0] and guild.id == i[1]:
                    await crs.execute(f"""DELETE FROM ROLES WHERE memberID = {i[0]}""")
                    await db.commit()
                    break
    
async def createbal(member):
    async with aiosqlite.connect('db.db') as db:
        await db.execute(sqlb)
        async with db.cursor() as crs:
            await crs.execute("""INSERT INTO BALANCE (memberID, balance) VALUES (:memberID, :balanceval)""", {'memberID': member.id, 'balanceval': 0})
            await db.commit()

async def checkbal(member):
    async with aiosqlite.connect('db.db') as db:
        await db.execute(sqlb)
        async with db.cursor() as crs:
            await crs.execute("""SELECT memberID, balance FROM BALANCE""")
            vals = await crs.fetchall()  
            for i in vals:
                if member.id == i[0]:
                    return i[1]
        return False           

async def balleader(member):
    async with aiosqlite.connect('db.db') as db:
        count = 1
        await db.execute(sqlb)
        async with db.cursor() as crs:
            await crs.execute("""SELECT memberID, balance FROM BALANCE ORDER BY balance DESC""")
            vals = await crs.fetchall()  
            for i in vals:
                if member.id == i[0]:
                    return count
                else:
                    count += 1      

async def addbal(member, amount):
    async with aiosqlite.connect('db.db') as db:
        await db.execute(sqlb)
        async with db.cursor() as crs:
            await crs.execute("""SELECT memberID, balance FROM BALANCE""")
            vals = await crs.fetchall()  
            for i in vals:
                if i[0] == member.id:
                    old = i[1]
                    tnew = old + amount
                    new = round(tnew, 2)
                    await crs.execute(f"""UPDATE BALANCE SET balance = {new} WHERE memberID = {member.id}""")
                    await db.commit()
                    break

async def removebal(member, amount):
    async with aiosqlite.connect('db.db') as db:
        await db.execute(sqlb)
        async with db.cursor() as crs:
            await crs.execute("""SELECT memberID, balance FROM BALANCE""")
            vals = await crs.fetchall()  
            for i in vals:
                if i[0] == member.id:
                    old = i[1]
                    tnew = old - amount
                    new = round(tnew, 2)
                    await crs.execute(f"""UPDATE BALANCE SET balance = {new} WHERE memberID = {member.id}""")
                    await db.commit()
                    break

async def addbank(amount):
    async with aiosqlite.connect('db.db') as db:
        await db.execute(sqlg)
        async with db.cursor() as crs:
            await crs.execute("""SELECT balance FROM BANK""")
            vals = await crs.fetchall()  
            for i in vals:
                old = i[0]
                tnew = old + amount
                new = round(tnew, 2)
                await crs.execute(f"""UPDATE BANK SET balance = {new}""")
                await db.commit()
                break

async def removebank(amount):
    async with aiosqlite.connect('db.db') as db:
        await db.execute(sqlg)
        async with db.cursor() as crs:
            await crs.execute("""SELECT balance FROM BANK""")
            vals = await crs.fetchall()  
            for i in vals:
                old = i[0]
                tnew = old - amount
                new = round(tnew, 2)
                await crs.execute(f"""UPDATE BANK SET balance = {new}""")
                await db.commit()
                break

async def getbankval():
     async with aiosqlite.connect('db.db') as db:
        await db.execute(sqlg)
        async with db.cursor() as crs:
            await crs.execute("""SELECT balance FROM BANK""")
            vals = await crs.fetchall()  
            for i in vals:
                return i[0]

async def lead():
    async with aiosqlite.connect('db.db') as db:
        await db.execute(sqlb)
        async with db.cursor() as crs:
            await crs.execute("""SELECT memberID, balance FROM BALANCE ORDER BY balance DESC""")
            vals = await crs.fetchall()  
            return vals

async def createcchannel(channel):
    async with aiosqlite.connect('db.db') as db:
        await db.execute(sqlt)
        async with db.cursor() as crs:
            await crs.execute("""INSERT INTO CRYPTO (channelid, guildid) VALUES (:channelID, :guildID)""", {'channelID': channel.id, 'guildID': channel.guild.id})
            await db.commit()

async def updatetime(channel, time):
    async with aiosqlite.connect('db.db') as db:
        await db.execute(sqlt)
        async with db.cursor() as crs:
            await crs.execute("""SELECT channelid, guildid, time FROM CRYPTO""")
            vals = await crs.fetchall()
            for i in vals:
                if channel.id == i[0] and channel.guild.id == i[1]:
                    await crs.execute(f"""UPDATE CRYPTO SET time = {time} WHERE guildid = {channel.guild.id}""")
                    await db.commit()
                    break

async def checktime(channel):
     async with aiosqlite.connect('db.db') as db:
        await db.execute(sqlt)
        async with db.cursor() as crs:
            await crs.execute("""SELECT channelid, time FROM CRYPTO""")
            vals = await crs.fetchall()
            for i in vals:
                if i[0] == channel.id:
                    return i[1]