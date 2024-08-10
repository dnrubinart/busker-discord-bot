import os

from discord.ext import commands
from stability_sdk import client


class Art(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stability_api = client.StabilityInference(
            key=os.environ["STABILITY_API_KEY"],
            verbose=True,
        )
