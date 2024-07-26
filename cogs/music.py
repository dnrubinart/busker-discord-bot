import discord, asyncio
from discord.ext import commands
from yt_dlp import YoutubeDL
import urllib.parse, urllib.request, re


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}
        self.voice_clients = {}
        self.youtube_base_url = "https://www.youtube.com/"
        self.youtube_results_url = self.youtube_base_url + "results?"
        self.youtube_watch_url = self.youtube_base_url + "watch?v="
        self.YTDL_OPTIONS = {"format": "bestaudio/best", "noplaylist": True}
        self.ytdl = YoutubeDL(self.YTDL_OPTIONS)
        self.FFMPEG_OPTIONS = {"before_options": 
                               "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", 
                               "options": "-vn -filter:a 'volume=0.25'"}
        
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} is now playing!")


    async def play_next(self, ctx):
        if self.queues[ctx.guild.id]:
            link = self.queues[ctx.guild.id].pop(0)
            await self.play(ctx, link=link)


    @commands.command(name="play")
    async def play(self, ctx, *, link):
        try:
            if ctx.guild.id in self.voice_clients and self.voice_clients[ctx.guild.id].is_connected():
                voice_client = self.voice_clients[ctx.guild.id]
            else:
                voice_client = await ctx.author.voice.channel.connect()
                self.voice_clients[ctx.guild.id] = voice_client

            if self.youtube_base_url not in link:
                query_string = urllib.parse.urlencode({"search_query": link})
                content = urllib.request.urlopen(self.youtube_results_url + query_string)
                search_results = re.findall(r"/watch\?v=(.{11})", content.read().decode())
                link = self.youtube_watch_url + search_results[0]

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(link, download=False))
            song = data["url"]
            player = discord.FFmpegOpusAudio(song, **self.FFMPEG_OPTIONS)

            if self.voice_clients[ctx.guild.id].is_playing() or self.voice_clients[ctx.guild.id].is_paused():
                if ctx.guild.id not in self.queues:
                    self.queues[ctx.guild.id] = []
                self.queues[ctx.guild.id].append(link)
                await ctx.send(f"Song added to the queue: {data['title']}")
            else:
                self.voice_clients[ctx.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))
                await ctx.send(f"Now playing: {data['title']}")
        except Exception as e:
            print(e)