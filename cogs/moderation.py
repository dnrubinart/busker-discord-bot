import discord, datetime
from discord.ext import commands


class Moderation(commands.Cog):
    

    @commands.has_any_role("Admin", "Moderator")
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if reason is None:
            reason = "This user has been kicked by" + ctx.author.name
        await member.kick(reason=reason)


    @commands.has_any_role("Admin", "Moderator")
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if reason is None:
            reason = "This user has been banned by" + ctx.author.name
        await member.ban(reason=reason)


    @commands.has_any_role("Admin", "Moderator")
    async def timeout(self, ctx, member: discord.Member, timelimit):
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