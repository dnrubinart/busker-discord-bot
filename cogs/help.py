import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    def help_message(self):
        return f""" ```
Music Commands:
!play <song> - Plays a song.
!pause - Pauses the current song.
!resume - Resumes the current song.
!skip - Skips the current song.
!clear - Clears the queue.
!disconnect - Disconnects the bot from the voice channel.
        
Moderation Commands:
!kick <member> - Kicks a member.
!ban <member> - Bans a member.
!timeout <member> <time> - Times out a member.
!rtimeout <member> - Removes a timeout from a member.
``` """

    
    @commands.command(name="help")
    async def help(self, ctx):
        await ctx.send(self.help_message())