# import discord
# from discord.ext import commands
# import logging
# from dotenv import load_dotenv
# import os

# load_dotenv()
# token = os.getenv('DISCORD_TOKEN')

# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# intentions = discord.Intents.default()
# intentions.message_content = True
# intentions.members = True

# bot = commands.Bot(command_prefix='!', intents=intentions)

# @bot.event
# async def on_ready():
#     print(f'We are ready to go in, {bot.user.name}')


# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
    
#     await bot.process_commands(message)


# @bot.command()
# async def hello(ctx):
#     await ctx.send(f'Hello, {ctx.author.name}!')


# bot.run(token, log_handler=handler, log_level=logging.DEBUG)


import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from rag import answer_question

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot ready as {bot.user.name}")

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.name}!')

@bot.command()
async def ask(ctx, *, question: str):
    answer = answer_question(question)
    await ctx.send(answer)

bot.run(token, log_handler=handler, log_level=logging.INFO)
