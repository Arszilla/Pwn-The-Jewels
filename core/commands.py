from asyncio import sleep

import discord
from discord.ext import commands



class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, context):
        """
        The typical help command for the bot. The actual print message 
        has been overwritten to this in __main__.py
        """

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
        from the channel it was invoked in
        """

        # Notify the user(s) about the purge
        await context.send(f"Clearing message(s)")

        # Give them a small timeframe to know
        await sleep(0.75)

        # Increase the amout by 2; because of the message sent by the
        # invoker and the message we just sent
        amount = int(amount) + 2

        deleted_amount = await context.channel.purge(limit=amount)

        # Let the user(s) know that the purge has happened, then
        # delete the information after a small timeframe
        await context.send(f"Cleared {len(deleted_amount)} message(s)",
                           delete_after=1.0)


def setup(bot):
    bot.add_cog(Commands(bot))
