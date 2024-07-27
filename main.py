import os, asyncio, discord
from discord.ext import commands
from dotenv import load_dotenv
from cogs.music import Music
from cogs.moderation import Moderation


load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

async def run_bot():
    async with bot:
        await bot.add_cog(Music(bot))
        await bot.add_cog(Moderation(bot))
        await bot.start(os.getenv("TOKEN"))

asyncio.run(run_bot())