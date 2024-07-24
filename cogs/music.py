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
        self.YDL_OPTIONS = {"format": "bestaudio", "noplaylist": "True"}
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
        if len(self.queue) > 0:
            self.is_playing = True
            music_url = self.queue[0][0]["source"]
            self.queue.pop(0)
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, self.search_yt, music_url)
            song = data["url"]
            self.voice_channel.play(discord.FFmpegPCMAudio(song, executable="ffmpeg.exe", **self.FFMPEG_OPTIONS), 
                                    after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))
        else:
            self.is_playing = False


    async def play_music(self, ctx):
        if len(self.queue) > 0:
            self.playing = True
            music_url = self.queue[0][0]["source"]
            if self.voice_channel == None:
                self.voice_channel = await self.queue[0][1].connect()
                if self.voice_channel == None:
                    await ctx.send("Couldn't join the voice channel.")
                    return
            else:
                await self.voice_channel.move_to(self.queue[0][1])
            self.queue.pop(0)
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, self.search_yt, music_url)
            song = data["url"]
            self.voice_channel.play(discord.FFmpegPCMAudio(song, executable="ffmpeg.exe", **self.FFMPEG_OPTIONS), 
                                    after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))
        else:
            self.is_playing = False


    @commands.command(name="play", aliases=["p"])
    async def play(self, ctx, *args):
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel
        if voice_channel == None:
            await ctx.send("You need to be in a voice channel to play music.")
        else:
            song = self.search_yt(query)
            self.queue.append([song, voice_channel])
            if self.is_playing == False:
                await self.play_music(ctx)
            else:
                await ctx.send(f"Added {song["title"]} to the queue.")