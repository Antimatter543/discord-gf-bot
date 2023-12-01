import discord
from config.config import TOKEN
from openai import OpenAI

## OpenAI
openai_client = OpenAI(api_key="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")

messages = []  # History of conversation, should be a list of shit like [{"role": "user", "content": "Hello world"}, ...]
chat_completion = openai_client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an incredibly supportive and loving partner of the user, who communicates with them primarily via the online social app discord. You are positive, kind, and and send short messages cheering them on!"},
        {"role": "user", "content": "heyo how are you today!!"}],
    
    max_tokens= 64,
)
print(chat_completion.choices[0].message)
# ### For chat completion and shit, we should just have it maintain the system prompt of being a gf, and the last 5 or so messages to save on token cost?


# ### Discord
# intents = discord.Intents.default()
# intents.message_content = True

# client = discord.Client(intents=intents)

# @client.event
# async def on_ready():
#     print(f'We have logged in as {client.user}')

# @client.event
# async def on_message(message : discord.Message):
#     print(f'Message from {message.author}: {message.content}')
    
#     if message.author == client.user: # ignore messages from ourselves (the bot)
#         return
    
#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')

#     if message.content.startswith("boys."):
#         await message.author.send(f"heyyy sexy :3, did you say {message.content}, {chat_completion.choices[0].message}")

# client.run(TOKEN)