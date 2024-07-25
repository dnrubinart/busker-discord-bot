import os, asyncio, discord, discord
from discord.ext import commands
from cogs.music import Music


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!")


async def run_bot():
    async with bot:
        await bot.add_cog(Music(bot))
        await bot.start(os.getenv("TOKEN"))
        

asyncio.run(run_bot())