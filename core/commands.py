from asyncio import sleep

import discord
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, context):
        embed = discord.Embed(
            title="Available Commands",
            type="rich",
            color=0x7CFC00
        )
        embed.add_field(
            name="help",
            value="Runs this command",
            inline=False
        )
        embed.add_field(
            name="clear",
            value="Clears a given amount of messages from the channel the command was invoked in",
            inline=False
        )

        await context.send(embed=embed)

    @commands.command()
    async def clear(self, context, amount):
        """
        This allows the invoker to delete any given number of messages
        """

        await context.send(f"Clearing message(s)")
        await sleep(0.75)
        amount = int(amount) + 2

        deleted_amount = await context.channel.purge(limit=amount)

        await context.send(f"Cleared {len(deleted_amount)} message(s)",
                           delete_after=1.0)


def setup(bot):
    bot.add_cog(Commands(bot))
