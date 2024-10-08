from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def help_message(self):
        """Returns a message containing the bot's commands."""
        return f"""
**Music Commands**:
{self.bot.command_prefix}play <song> - Plays a song by providing a search query or a link.
{self.bot.command_prefix}pause - Pauses the current song.
{self.bot.command_prefix}resume - Resumes the current song.
{self.bot.command_prefix}skip - Skips the current song.
{self.bot.command_prefix}queue - Shows the current queue.
{self.bot.command_prefix}clear - Clears the queue.
{self.bot.command_prefix}disconnect - Disconnects the bot from the voice channel. \n
**Generation Commands**:
{self.bot.command_prefix}draw <prompt> - Generates an image based on the provided prompt.
{self.bot.command_prefix}ask <prompt> - Generates a response based on the provided prompt. \n
"""

    def admin_help_message(self):
        """Returns a message containing the bot's admin commands."""
        return f"""
**Moderation Commands**:
{self.bot.command_prefix}kick <member> - Kicks a member.
{self.bot.command_prefix}ban <member> - Bans a member.
{self.bot.command_prefix}unban <member> - Unbans a member.
{self.bot.command_prefix}timeout <member> <time> - Times out a member.
{self.bot.command_prefix}rmtimeout <member> - Removes a timeout from a member.
"""

    @commands.command(name="help")
    async def help(self, ctx):
        """Displays the bot's commands."""
        await ctx.send(self.help_message())

    @commands.command(name="adminhelp", aliases=["ahelp"])
    @commands.has_permissions(administrator=True)
    async def admin_help(self, ctx):
        """Displays the bot's admin commands."""
        await ctx.send(self.admin_help_message())
