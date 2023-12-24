from typing import Any
import discord
from discord.flags import Intents
from config.config import DISCORD_TOKEN, OPENAI_TOKEN, SYSTEM_PROMPT
from openai import OpenAI

import io
from mcstatus import JavaServer



# TODO : Refactor the shit above to be below. see gpt
class DiscordPartner(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = {} # Could convert to a dictionary which maps user id -> message history

        self.openai_client = OpenAI(api_key=OPENAI_TOKEN)

        
    async def on_ready(self):
        print(f'We have logged in as {self.user}')

    async def on_message(self, message : discord.Message):
        print(f'Message from {message.author}: {message.content}')
        
        if message.author == self.user: # ignore messages from ourselves (the bot)
            return
        
        if message.content.startswith('helloa'):
            # print(message.author)
            await message.channel.send('Hello aaaaa!')
        # elif message.content.startswith('$'):

        if message.content.startswith("/mcstatus"):
            
            server = JavaServer.lookup("minecraft.uqcs.org:25605")


            status = server.status()
            print(status.players)
            await message.channel.send(f"The server has {status.players.online} player(s) online:  {status.players} and replied in {status.latency} ms")

        else:
            await self.response(message)

    async def response(self, discord_message: discord.Message):
        if self.messages.get(discord_message.author) == None:
            self.messages[discord_message.author] = [{"role": "system", "content": SYSTEM_PROMPT}] 
        self.messages[discord_message.author].append({"role": "user", "content": discord_message.content})

        chat_completion = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages= self.messages[discord_message.author],
            # max_tokens= 300, 
        )


        print("Message loaded")
        ### For chat completion and shit, we should just have it maintain the system prompt of being a gf, and the last 5 or so messages to save on token cost?
        response_message : str = chat_completion.choices[0].message.content
        # if discord_message.content.startswith('hi'):
        #     response_message = "yoooooo testestsetsetts t"
        # else:
        #     response_message = "yoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts ttyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts tyoooooo testestsetsetts t"
        self.messages[discord_message.author].append({"role": "assistant", "content": response_message})

        print(f"So {discord_message.author} sent: {discord_message.content}\n and received: {response_message}\n")
        ### TODO: Check if chat completion message is > 2000 char length, and if so then send as a file instead.
        if len(response_message) > 1900: # 1900 just in case :) 
            # Create a file-like object from the response message
            with io.BytesIO(response_message.encode('utf-8')) as buffer:
                buffer.seek(0)
                await discord_message.channel.send(file=discord.File(fp=buffer, filename="response.txt"))
        
        else:
            await discord_message.author.send(response_message)

        # await discord_message.channel.send(response_message)

# Initialize and run the bot
intents = discord.Intents.default()
intents.message_content = True
bot = DiscordPartner(intents=intents)
bot.run(DISCORD_TOKEN)


