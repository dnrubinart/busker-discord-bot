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
        if item.startswith("https://www.youtube.com/"):
            title = self.yt_dl.extract_info(item, download=False)["title"]
            return {"source": item, "title": title}
        search = self.yt_dl.extract_info(f"ytsearch:{item}", download=False)["entries"][0]
        return {"source": search["formats"][0]["url"], "title": search["title"]}


    async def play_next(self):
        pass


    async def play_music(self):
        pass