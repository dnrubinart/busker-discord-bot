import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    def help_message(self):
        return f"""
**Music Commands**:
{self.bot.command_prefix}play <song> - Plays a song.
{self.bot.command_prefix}pause - Pauses the current song.
{self.bot.command_prefix}resume - Resumes the current song.
{self.bot.command_prefix}skip - Skips the current song.
{self.bot.command_prefix}clear - Clears the queue.
{self.bot.command_prefix}disconnect - Disconnects the bot from the voice channel.

**Moderation Commands**:
{self.bot.command_prefix}kick <member> - Kicks a member.
{self.bot.command_prefix}ban <member> - Bans a member.
{self.bot.command_prefix}timeout <member> <time> - Times out a member.
{self.bot.command_prefix}rtimeout <member> - Removes a timeout from a member.
"""

    
    @commands.command(name="help")
    async def help(self, ctx):
        await ctx.send(self.help_message())