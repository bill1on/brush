import discord
import asyncio
from discord.ext import commands
from utilsdb import sqlt

intents = discord.Intents.all()
client = commands.Bot(command_prefix= '.', intents = intents)
extensions = ['cogs.tooth', 'cogs.eco', 'cogs.crypto', 'cogs.kaiji']

ENABLE_CRYPTO = False

@client.event
async def on_ready():
    await sqlt.loopsql(client)
    if ENABLE_CRYPTO:
        await sqlt.loopcrypto(client)
    print('We have logged in as {0.user}'.format(client))

if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
        except:
            print("Couldn't load %s", extension)
    with open('token.txt', 'r') as f:
        token = f.read()
        client.run(token) # token.txt in folder
