import os
import asyncio
import discord
import logging
from discord.ext import commands
from dotenv import load_dotenv
from cogs.music import Music
from cogs.moderation import Moderation
from cogs.help import Help


logging.basicConfig(level=logging.INFO)
load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    print(f"{bot.user} is now online!")


async def run_bot():
    async with bot:
        await bot.add_cog(Music(bot))
        await bot.add_cog(Moderation(bot))
        await bot.add_cog(Help(bot))
        await bot.start(os.getenv("TOKEN"))

asyncio.run(run_bot())