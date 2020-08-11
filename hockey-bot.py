import os
import discord
import HBMRclass

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

messagerouter = HBMRclass.HBMR()

@client.event
async def on_ready():
    print(f'{client.user} has connected.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content[0:2] == 'HB':
        result = messagerouter.route(message.content)
        if result:
            await message.channel.send(result)

client.run(TOKEN)