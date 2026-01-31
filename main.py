import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from rag import answer_question
import time

load_dotenv()
token = os.getenv("DISCORD_TOKEN")


instance_id = int(time.time() * 1000) % 10000

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
    try:
        answer = answer_question(question)
        await ctx.send(answer)
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

if __name__ == "__main__":
    bot.run(token, log_handler=handler, log_level=logging.INFO)