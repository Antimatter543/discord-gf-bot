import discord
from config.config import TOKEN


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message : discord.Message):
    print(f'Message from {message.author}: {message.content}')
    
    if message.author == client.user: # ignore messages from ourselves (the bot)
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


client.run(TOKEN)