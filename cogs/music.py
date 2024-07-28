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
                               "options": 
                               "-vn -filter:a 'volume=0.25'"}


    async def play_next(self, ctx):
        if self.queues[ctx.guild.id]:
            link = self.queues[ctx.guild.id].pop(0)
            await self.play(ctx, link=link)


    @commands.command(name="play", aliases=["p"])
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
                await ctx.send(f"Song added to the queue: **{data['title']}**")
            else:
                self.voice_clients[ctx.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))
                await ctx.send(f"Now playing: **{data['title']}**")
        except Exception as e:
            print(e)

        
    @commands.command(name="pause")
    async def pause(self, ctx):
        try:
            self.voice_clients[ctx.guild.id].pause()
        except Exception as e:
            print(e)

    
    @commands.command(name="resume")
    async def resume(self, ctx):
        try:
            self.voice_clients[ctx.guild.id].resume()
        except Exception as e:
            print(e)


    @commands.command(name="skip")
    async def skip(self, ctx):
        try:
            self.voice_clients[ctx.guild.id].stop()
            await self.play_next(ctx)
        except Exception as e:
            print(e)


    @commands.command(name="queue", aliases=["q"])
    async def queue(self, ctx):
        if ctx.guild.id in self.queues:
            queue_list = ""
            for i, link in enumerate(self.queues[ctx.guild.id]):
                data = self.ytdl.extract_info(link, download=False)
                queue_list += f"{i + 1}: {data['title']}\n"
            await ctx.send(f"**Current songs in the queue**:\n{queue_list}")
        else:
            await ctx.send("There are no songs in the queue.")


    @commands.command(name="clear")
    async def clear(self, ctx):
        if ctx.guild.id in self.queues:
            self.queues[ctx.guild.id].clear()
            await ctx.send("Queue has been cleared.")
        else:
            await ctx.send("There are no songs in the queue.")

    
    @commands.command(name="disconnect", aliases=["dc"])
    async def disconnect(self, ctx):
        try:
            self.voice_clients[ctx.guild.id].stop()
            await self.voice_clients[ctx.guild.id].disconnect()
            del self.voice_clients[ctx.guild.id]
            if ctx.guild.id in self.queues:
                self.queues[ctx.guild.id].clear()
        except Exception as e:
            print(e)