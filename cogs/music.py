import discord, asyncio
from discord.ext import commands
from yt_dlp import YoutubeDL


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.is_playing = False
        self.is_paused = False
        self.voice_channel = None
        self.YDL_OPTIONS = {"format": "bestaudio", "noplaylist":"True"}
        self.FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                               "options": "-vn -filter:a volume=0.25"}
        self.yt_dl = YoutubeDL(self.YDL_OPTIONS)

    def search_yt(self, item):
        pass


    async def play_next(self):
        pass


    async def play_music(self):
        pass