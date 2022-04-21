from discord.ext import commands
import discord


def is_admin():
    return commands.check_any(
        commands.is_owner(), commands.has_permissions(administrator=True)
    )


def is_banker():
    async def predicate(ctx):
        try:
            is_banker = ctx.guild.get_role(929227238166114306) in ctx.author.roles
        except AttributeError:
            return False

        if not is_banker:
            raise commands.CheckFailure(f"You are not a banker.")
        return is_banker

    return commands.check(predicate)


def has_started():
    async def predicate(ctx):
        member = await ctx.bot.mongo.Member.find_one(
            {"id": ctx.author.id}, {"suspended": 1, "suspension_reason": 1}
        )
        
        if member is None:
            embed=discord.Embed(title="New Account", description=f"Please register by doing `{ctx.prefix}start`\nNote: Running this command means you have accepted our [Terms of Service](https://poketox.me/tos)", color=0x36393F)
            await ctx.send(embed=embed)
            raise commands.CheckFailure(None)

        if member.suspended:
            embed=discord.Embed(title="Account Suspended", description="Your account was found to be in violation of Pokétox rules and has been permanently blacklisted from using the bot.", color=0xe74d3c)
            embed.add_field(name="Reason", value=member.suspension_reason, inline=False)
            await ctx.send(embed=embed)
            raise commands.CheckFailure(None)
           

        return True

    return commands.check(predicate)


def in_event():
    async def predicate(ctx):
        member = await ctx.bot.mongo.Member.find_one({"id": ctx.author.id})

        if member is None:
            raise commands.CheckFailure(
                f"Please first start by running `{ctx.prefix}start`!"
            )

        if not member.event_activated:
            raise commands.CheckFailure(
                f"You need to join the event with `{ctx.prefix}event join`"
            )

        return True

    return commands.check(predicate)
