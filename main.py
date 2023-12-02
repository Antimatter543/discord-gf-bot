import discord
from config.config import TOKEN, OPENAI_TOKEN, SYSTEM_PROMPT
from openai import OpenAI

messages = []
async def response(discord_message: discord.Message):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.append({"role": "user", "content": discord_message.content})
    chat_completion = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages= messages,
        
        max_tokens= 128,
    )
    print("Message loaded")
     ### For chat completion and shit, we should just have it maintain the system prompt of being a gf, and the last 5 or so messages to save on token cost?
    response_message : str = chat_completion.choices[0].message.content

    messages.append({"role": "assistant", "content": response_message})
    print(f"messages here {messages}")
    await discord_message.author.send(response_message)

## OpenAI
openai_client = OpenAI(api_key=OPENAI_TOKEN)

messages = []  # History of conversation, should be a list of shit like 

### Discord
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

    if message.content.startswith("hii"):
        await response(message)

client.run(TOKEN)


    