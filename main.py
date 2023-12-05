from typing import Any
import discord
from discord.flags import Intents
from config.config import DISCORD_TOKEN, OPENAI_TOKEN, SYSTEM_PROMPT
from openai import OpenAI





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
        else:
            await self.response(message)

    async def response(self, discord_message: discord.Message):
        if self.messages.get(discord_message.author) == None:
            self.messages[discord_message.author] = [{"role": "system", "content": SYSTEM_PROMPT}] 
        self.messages[discord_message.author].append({"role": "user", "content": discord_message.content})

        chat_completion = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages= self.messages[discord_message.author],
            
            max_tokens= 256,
        )
        print("Message loaded")
        ### For chat completion and shit, we should just have it maintain the system prompt of being a gf, and the last 5 or so messages to save on token cost?
        response_message : str = chat_completion.choices[0].message.content

        self.messages[discord_message.author].append({"role": "assistant", "content": response_message})
        # print(f"messages here {self.messages}")

        print(f"So {discord_message.author} sent: {discord_message.content}\n and received: {response_message}\n")
        
        await discord_message.author.send(response_message)
        # await discord_message.author.send(response_message)
# Initialize and run the bot
intents = discord.Intents.default()
intents.message_content = True
bot = DiscordPartner(intents=intents)
bot.run(DISCORD_TOKEN)


