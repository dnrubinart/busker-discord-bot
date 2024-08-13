import datetime

import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks a member from the server."""
        if reason is None:
            reason = "This user has been kicked by " + ctx.author.name
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="Member kicked.",
            description=f"{member.mention} has been kicked.",
            color=discord.Color.red(),
        )
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Bans a member from the server."""
        if reason is None:
            reason = "This user has been banned by " + ctx.author.name
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="Member banned.",
            description=f"{member.mention} has been banned.",
            color=discord.Color.red(),
        )
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member: str):
        """Unbans a member from the server."""
        banned_users = []
        async for entry in ctx.guild.bans():
            banned_users.append(entry)

        for ban_entry in banned_users:
            user = ban_entry.user
            if user.name == member:
                await ctx.guild.unban(user)
                embed = discord.Embed(
                    title="Member unbanned.",
                    description=f"{user.mention} has been unbanned.",
                    color=discord.Color.green(),
                )
                await ctx.send(embed=embed)
                return
        await ctx.send(f"{member} is not banned.")

    @commands.command(name="timeout")
    @commands.has_permissions(kick_members=True)
    async def timeout(self, ctx, member: discord.Member, timelimit):
        """Timeout a member for a specified time. The time limit can be in seconds, minutes, hours or days."""
        if "s" in timelimit:
            get_time = timelimit.replace("s", "")
            if int(get_time) > 2419000:
                await ctx.send("You cannot timeout for more than 28 days.")
            else:
                timeout_time = datetime.timedelta(seconds=int(get_time))
                await member.edit(timed_out_until=discord.utils.utcnow() + timeout_time)
        elif "m" in timelimit:
            get_time = timelimit.replace("m", "")
            if int(get_time) > 40320:
                await ctx.send("You cannot timeout for more than 28 days.")
            else:
                timeout_time = datetime.timedelta(minutes=int(get_time))
                await member.edit(timed_out_until=discord.utils.utcnow() + timeout_time)
        elif "h" in timelimit:
            get_time = timelimit.replace("h", "")
            if int(get_time) > 672:
                await ctx.send("You cannot timeout for more than 28 days.")
            else:
                timeout_time = datetime.timedelta(hours=int(get_time))
                await member.edit(timed_out_until=discord.utils.utcnow() + timeout_time)
        elif "d" in timelimit:
            get_time = timelimit.replace("d", "")
            if int(get_time) > 28:
                await ctx.send("You cannot timeout for more than 28 days.")
            else:
                timeout_time = datetime.timedelta(days=int(get_time))
                await member.edit(timed_out_until=discord.utils.utcnow() + timeout_time)
        embed = discord.Embed(
            title="Member timed out.",
            description=f"{member.mention} has been timed out for {timelimit}.",
            color=discord.Color.orange(),
        )
        await ctx.send(embed=embed)

    @commands.command(name="rmtimeout")
    @commands.has_permissions(kick_members=True)
    async def rtimeout(self, ctx, member: discord.Member):
        """Removes the timeout from a member."""
        await member.edit(timed_out_until=None)
        embed = discord.Embed(
            title="Timeout removed.",
            description=f"{member.mention}'s timeout has been removed.",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)
