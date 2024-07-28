import discord, datetime
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name="kick")
    @commands.has_any_role("Administrator", "Moderator")
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if reason is None:
            reason = "This user has been kicked by" + ctx.author.name
        await member.kick(reason=reason)


    @commands.command(name="ban")
    @commands.has_any_role("Administrator", "Moderator")
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if reason is None:
            reason = "This user has been banned by" + ctx.author.name
        await member.ban(reason=reason)


    @commands.command(name="unban")
    @commands.has_any_role("Administrator", "Moderator")
    async def unban(self, ctx, *, member: str):
        banned_users = []
        async for entry in ctx.guild.bans():
            banned_users.append(entry)

        for ban_entry in banned_users:
            user = ban_entry.user
            if user.name == member:
                await ctx.guild.unban(user)
                await ctx.send(f"{user.mention} has been unbanned.")
                return
        await ctx.send(f"{member} is not banned.")


    @commands.command(name="timeout")
    @commands.has_any_role("Administrator", "Moderator")
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


    @commands.command(name="rmtimeout")
    @commands.has_any_role("Administrator", "Moderator")
    async def rtimeout(self, ctx, member: discord.Member):
        await member.edit(timed_out_until=None)