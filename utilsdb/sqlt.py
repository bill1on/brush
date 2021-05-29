import aiosqlite
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from cogs import tooth
from cogs import crypto

def maindb(guildID):
    sqldb = f"""CREATE TABLE IF NOT EXISTS MAIN{str(guildID)} (
                memberID integer PRIMARY KEY,
                guildID int,
                balance float,
                brushedt int,
                rolelist TEXT
            )"""
    return sqldb

def bankdb(guildID):
    sqldbb = f"""CREATE TABLE IF NOT EXISTS BANK{guildID}(
                balance float
    )"""
    return sqldbb

def cryptodb(guildID):
    sqlt = f"""CREATE TABLE IF NOT EXISTS CRYPTO{guildID} (
                channelid integer,
                guildid integer,
                time integer
    )"""
    return sqlt

def shopdb(guildID):
    sqls = f"""CREATE TABLE IF NOT EXISTS SHOP{guildID} (
                memberid integer,
                guildid integer,
                name,
                value,
                price integer
    )"""
    return sqls

async def maket(guild, member): #updates the boolean value "brushed" to True of the given user 'member'
    async with aiosqlite.connect('db.db') as db:
        await db.execute(maindb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT memberID, guildID, brushedt FROM MAIN{guild.id}""")
            vals = await crs.fetchall()
            for i in vals:
                if member.id == i[0] and guild.id == int(i[1]):
                    val = 1
                    await crs.execute(f"""UPDATE MAIN{guild.id} SET brushedt = {val} WHERE memberID = {i[0]}""")
                    await db.commit()
                    break # D

async def loopsql(bot): #loop which is run everytime the bot starts to make sure that the users in the database are running the task
    async with aiosqlite.connect("db.db") as db:
        async with db.cursor() as crs:
            await crs.execute("SELECT name FROM sqlite_master WHERE type= 'table';")
            tlist = await crs.fetchall()
            for i in tlist:
                if i[0].startswith('MAIN'):
                    await crs.execute(f"""SELECT memberID, guildID FROM {i[0]}""")
                    dat = await crs.fetchall()
                    for i in dat:
                        server = bot.get_guild(i[1])
                        member = server.get_member(i[0])
                        tooth.Tooth(bot).lockt.start(member, server) # -------------------------------MAJOR QUESTION MARK COME BACK LATER

async def makef(guild, member): #makes the boolean value 'brushed' False in the database
    async with aiosqlite.connect('db.db') as db:
        await db.execute(maindb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT memberID, guildID, brushedt FROM MAIN{guild.id}""")
            vals = await crs.fetchall()
            for i in vals:
                if member.id in i and guild.id in i:
                    val = 0
                    await crs.execute(f"""UPDATE MAIN{guild.id} SET brushedt = {val} WHERE memberID = {i[0]}""")
                    await db.commit()
                    break # D

async def checkb(guild, member): #checks whether the boolean value "brushed" is True or False
    async with aiosqlite.connect('db.db') as db:
        await db.execute(maindb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT memberID, guildID, brushedt FROM MAIN{guild.id}""")
            vals = await crs.fetchall()
            for i in vals:
                if member.id in i and guild.id in i:
                    if i[2] == 0:
                        return False
                    elif i[2] == 1:
                        return True #D

async def checkt(guild, member): # checks whether a person is in the database
    async with aiosqlite.connect('db.db') as db:
        await db.execute(maindb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT memberID, guildID FROM MAIN{str(guild.id)}""")
            vals = await crs.fetchall()  
            for i in vals:
                if member.id in i and guild.id in i:
                    return True
            return False  #D
 
async def addt(guild, member): #adds the person to the database
    async with aiosqlite.connect('db.db') as db:
        await db.execute(maindb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""INSERT INTO MAIN{guild.id} (guildID, memberID, balance, brushedt) VALUES (:guildID, :memberID, :balance, :brushedval)""", {'guildID': guild.id, 'memberID': member.id, 'balance': 0, 'brushedval': False})
            await db.commit() #D

async def roleadd(guild, member, rlist): #adds the list of roles to the database that the user currently has
    async with aiosqlite.connect('db.db') as db:
        await db.execute(maindb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""UPDATE MAIN{guild.id} SET rolelist = {rlist} WHERE memberID = {member.id}""")
            await db.commit() #D

async def roleget(guild, member): # fetches the roles from the database
    async with aiosqlite.connect('db.db') as db:
        await db.execute(maindb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT memberID, guildID, rolelist FROM MAIN{guild.id}""")
            vals = await crs.fetchall()
            for i in vals:
                if member.id == i[0] and guild.id == i[1]:
                    return i[2] #D

async def checkrole(guild, member): # checks if the user is in the roles database
    async with aiosqlite.connect('db.db') as db:
        await db.execute(maindb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT memberID, guildID, rolelist FROM MAIN{guild.id}""")
            vals = await crs.fetchall()
            for i in vals:
                if member.id == i[0] and guild.id == i[1]:
                    return True
                else:
                    return False #D

async def deleterole(guild, member): # deletes data from user from database
    async with aiosqlite.connect('db.db') as db:
        await db.execute(maindb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT memberID, guildID, rolelist FROM MAIN{guild.id}""")
            vals = await crs.fetchall()
            for i in vals:
                if member.id == i[0] and guild.id == i[1]:
                    await crs.execute(f"""UPDATE MAIN{guild.id} SET rolelist = NULL WHERE memberID = {i[0]}""")
                    await db.commit()
                    break #D

async def checkbal(guild, member):
    async with aiosqlite.connect('db.db') as db:
        await db.execute(maindb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT memberID, balance FROM MAIN{guild.id}""")
            vals = await crs.fetchall()  
            for i in vals:
                if member.id == i[0]:
                    return i[1]
        return False #D

async def balleader(guild, member):
    async with aiosqlite.connect('db.db') as db:
        count = 1
        await db.execute(maindb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT memberID, balance FROM MAIN{guild.id} ORDER BY balance DESC""")
            vals = await crs.fetchall()  
            for i in vals:
                if member.id == i[0]:
                    return count
                else:
                    count += 1 #D

async def addbal(guild, member, amount):
    async with aiosqlite.connect('db.db') as db:
        await db.execute(maindb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT memberID, balance FROM MAIN{guild.id}""")
            vals = await crs.fetchall()  
            for i in vals:
                if i[0] == member.id:
                    old = i[1]
                    tnew = old + amount
                    new = round(tnew, 2)
                    await crs.execute(f"""UPDATE MAIN{guild.id} SET balance = {new} WHERE memberID = {member.id}""")
                    await db.commit()
                    break #D

async def removebal(guild, member, amount):
    async with aiosqlite.connect('db.db') as db:
        await db.execute(maindb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT memberID, balance FROM MAIN{guild.id}""")
            vals = await crs.fetchall()  
            for i in vals:
                if i[0] == member.id:
                    old = i[1]
                    tnew = old - amount
                    new = round(tnew, 2)
                    await crs.execute(f"""UPDATE MAIN{guild.id} SET balance = {new} WHERE memberID = {member.id}""")
                    await db.commit()
                    break #D

async def addbank(guild, amount):
    async with aiosqlite.connect('db.db') as db:
        await db.execute(bankdb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT balance FROM BANK{guild.id}""")
            vals = await crs.fetchall()  
            for i in vals:
                old = i[0]
                tnew = old + amount
                new = round(tnew, 2)
                await crs.execute(f"""UPDATE BANK{guild.id} SET balance = {new}""")
                await db.commit()
                break #D

async def createbank(guild):
     async with aiosqlite.connect('db.db') as db:
        await db.execute(bankdb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""INSERT INTO BANK{guild.id} (balance) VALUES (:balance)""", {'balance': 0})
            await db.commit() #D

async def removebank(guild, amount):
    async with aiosqlite.connect('db.db') as db:
        await db.execute(bankdb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT balance FROM BANK{guild.id}""")
            vals = await crs.fetchall()  
            for i in vals:
                old = i[0]
                tnew = old - amount
                new = round(tnew, 2)
                await crs.execute(f"""UPDATE BANK{guild.id} SET balance = {new}""")
                await db.commit()
                break #D

async def getbankval(guild):
     async with aiosqlite.connect('db.db') as db:
        await db.execute(bankdb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT balance FROM BANK{guild.id}""")
            vals = await crs.fetchall()  
            for i in vals:
                return i[0] #D

async def lead(guild):
    async with aiosqlite.connect('db.db') as db:
        await db.execute(maindb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT memberID, balance FROM MAIN{guild.id} ORDER BY balance DESC""")
            vals = await crs.fetchall()  
            return vals #D

async def createcchannel(channel):
    async with aiosqlite.connect('db.db') as db:
        await db.execute(cryptodb(channel.guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""INSERT INTO CRYPTO{channel.guild.id} (channelid, guildid) VALUES (:channelID, :guildID)""", {'channelID': channel.id, 'guildID': channel.guild.id})
            await db.commit() #D

async def updatetime(channel, time):
    async with aiosqlite.connect('db.db') as db:
        await db.execute(cryptodb(channel.guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT channelid, guildid, time FROM CRYPTO{channel.guild.id}""")
            vals = await crs.fetchall()
            for i in vals:
                if channel.id == i[0] and channel.guild.id == i[1]:
                    await crs.execute(f"""UPDATE CRYPTO{channel.guild.id} SET time = {time} WHERE guildid = {channel.guild.id}""")
                    await db.commit()
                    break #D

async def checktime(channel):
     async with aiosqlite.connect('db.db') as db:
        await db.execute(cryptodb(channel.guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT channelid, time FROM CRYPTO{channel.guild.id}""")
            vals = await crs.fetchall()
            if len(vals) == 0:
                return False
            else:
                for i in vals:
                    if i[0] == channel.id:
                        return i[1] #D
    
async def loopcrypto(bot):
    async with aiosqlite.connect("db.db") as db:
        async with db.cursor() as crs:
            await crs.execute("SELECT name FROM sqlite_master WHERE type= 'table';")
            tlist = await crs.fetchall()
            for i in tlist:
                if i[0].startswith('CRYPTO'):
                    await crs.execute(f"""SELECT channelid FROM {i[0]}""")
                    dat = await crs.fetchall()
                    for i in dat:
                        await crypto.whaletrans.start(bot.get_channel(i[0])) #--- COME BACK LATER MAJOR ISSUE

async def removecrypto(channel):
    async with aiosqlite.connect('db.db') as db:
        await db.execute(cryptodb(channel.guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT channelid FROM CRYPTO{channel.guild.id}""")
            await crs.execute(f"""DELETE FROM CRYPTO{channel.guild.id} WHERE channelid = {channel.id}""")
            await db.commit() #D
            
async def checkcrypto(channel):
    async with aiosqlite.connect('db.db') as db:
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT channelid FROM CRYPTO{channel.guild.id}""")
            vals = await crs.fetchall()
            if len(vals) >= 1:
                return True
            else:
                return False

async def checkshop(guild):
    async with aiosqlite.connect('db.db') as db:
        await db.execute(shopdb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT guildid FROM SHOP{guild.id}""")
            vals = await crs.fetchall()
            for i in vals:
                if i[0] == guild.id:
                    return True
            return False #D
            
async def auctionshop(member, guild, name, value, price):
    async with aiosqlite.connect('db.db') as db:
        await db.execute(shopdb(guild.id))
        async with db.cursor() as crs:
             await crs.execute(f"""INSERT INTO SHOP{guild.id} (memberid, guildid, name, value, price) VALUES (:memberID, :guildID, :name, :value, :price)""", {'memberID': member.id, 'guildID': guild.id, 'name': name, 'value': value, 'price': price})
             await db.commit() #D

async def getshop(guild):
    async with aiosqlite.connect('db.db') as db:
        await db.execute(shopdb(guild.id))
        async with db.cursor() as crs:
            rlist = []
            await crs.execute(f"""SELECT memberid, guildid, name, value, price FROM SHOP{guild.id}""")
            vals = await crs.fetchall()
            for i in vals:
                if i[1] == guild.id:
                    alist = [i[0], i[2], i[3], i[4]]
                    rlist.append(alist)
            return rlist #D

async def listingpermember(guild, member):
    async with aiosqlite.connect('db.db') as db:
        c = 0
        await db.execute(shopdb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT memberid FROM SHOP{guild.id}""")
            vals = await crs.fetchall()
            for i in vals:
                if i[0] == member.id:
                    c += 1
            return c #D

async def checkshopname(guild, name):
    async with aiosqlite.connect('db.db') as db:
        ilist = []
        await db.execute(shopdb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""SELECT memberid, guildid, name, value, price FROM SHOP{guild.id}""")
            vals = await crs.fetchall()
            for i in vals:
                if i[2] == name:
                    ilist.append(i)
            return ilist #D

async def removeshop(guild, list):
    async with aiosqlite.connect('db.db') as db:
        await db.execute(shopdb(guild.id))
        async with db.cursor() as crs:
            await crs.execute(f"""DELETE FROM SHOP{guild.id} WHERE name = '{list[2]}' AND memberid = {list[0]}""")
            await db.commit() #D
