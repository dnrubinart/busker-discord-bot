import discord
from discord.ext import commands


class Moderation(commands.Cog):
    
    @commands.has_any_role("Admin", "Moderator")
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if reason is None:
            reason = "This user has been kicked by" + ctx.author.name
        await member.kick(reason=reason)