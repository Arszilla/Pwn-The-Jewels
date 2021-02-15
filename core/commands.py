from asyncio import sleep
from os import makedirs
from os.path import isdir, isfile

import discord
from discord.ext import commands

from core import analyze, constants, functions, reddit


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
        embed.add_field(
            name="analyze_linux",
            value="Using `checksec.py`, analyze a given Linux binary",
            inline=False
        )
        embed.add_field(
            name="analyze_windows",
            value="Using `checksec.py`, analyze a given Windows binary",
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
        await context.send(f"Clearing message(s)...")

        # Give them a small timeframe to know
        await sleep(0.75)

        # Increase the amout by 2; because of the message sent by the
        # invoker and the message we just sent
        amount = int(amount) + 2

        deleted_amount = await context.channel.purge(limit=amount)

        # Let the user(s) know that the purge has happened, then
        # delete the information after a small timeframe
        await context.send(f"Cleared {len(deleted_amount)} message(s).",
                           delete_after=1.0)


    @commands.command()
    async def addsubreddit(self, context, subreddit):
        reddit_class = reddit.Reddit(bot=None)
        result = await reddit_class.add_subreddit(subreddit.lower())

        if result == False:
            await context.send(f"`/r/{subreddit.lower()}` subreddit already exists in the watchlist database, as a result it was not added.")

        elif result == True:
            await context.send(f"Added `/r/{subreddit.lower()}` subreddit to the watchlist database.")


    @commands.command()
    async def removesubreddit(self, context, subreddit):
        reddit_class = reddit.Reddit(bot=None)
        result = await reddit_class.remove_subreddit(subreddit.lower())

        if result == False:
            await context.send(f"`/r/{subreddit.lower()}` subreddit doesn't exist in the watchlist database, as a result it was not removed.")

        elif result == True:
            await context.send(f"Removed `/r/{subreddit.lower()}` subreddit from the watchlist database.")


    @commands.command()
    async def analyze_linux(self, context):
        """
        This allows the bot to download an attachment sent with the 
        'analyze_linux' command, then run certain commands to gather 
        more information about the sent binary, and then feed the 
        said information in an embed
        """

        functions.Functions().check_directory()

        # Get the filename
        filename = context.message.attachments[0].filename

        filename = functions.Functions().check_file(filename)

        await context.message.attachments[0].save(f"files/{filename}")

        file_analysis = analyze.Analysis()
        analysis_data = file_analysis.checksec(filename)

        embed = discord.Embed(
            title=f"File Analysis for {filename}",
            type="rich",
            description="**checksec**\n"
                        f"**RELRO:** {analysis_data[0]}\n"
                        f"**Canary:** {analysis_data[1]}\n"
                        f"**NX:** {analysis_data[2]}\n"
                        f"**PIE:** {analysis_data[3]}\n"
                        f"**RPATH:** {analysis_data[4]}\n"
                        f"**RunPath:** {analysis_data[5]}\n"
                        f"**Symbols:** {analysis_data[6]}\n"
                        f"**Fortify:** {analysis_data[7]}\n"
                        f"**Fortified:** {analysis_data[8]}\n"
                        f"**Fortibiable:** {analysis_data[9]}\n"
                        f"**Fortify Score:** {analysis_data[10]}\n",
            color=0xFB8B00
        )

        await context.send(embed=embed)

    @commands.command()
    async def analyze_windows(self, context):
        """
        This allows the bot to download an attachment sent with the 
        'analyze_linux' command, then run certain commands to gather 
        more information about the sent binary, and then feed the 
        said information in an embed
        """

        functions.Functions().check_directory()

        # Get the filename
        filename = context.message.attachments[0].filename

        filename = functions.Functions().check_file(filename)

        await context.message.attachments[0].save(f"files/{filename}")

        file_analysis = analyze.Analysis()
        analysis_data = file_analysis.checksec(filename)

        embed = discord.Embed(
            title=f"File Analysis for {filename}",
            type="rich",
            description="**checksec**\n"
                        f"**NX:** {analysis_data[0]}\n"
                        f"**Canary:** {analysis_data[1]}\n"
                        f"**ASLR:** {analysis_data[2]}\n"
                        f"**Dynamic Base:** {analysis_data[3]}\n"
                        f"**High Entropy VA:** {analysis_data[4]}\n"
                        f"**SEH:** {analysis_data[6]}\n"
                        f"**SafeSEH:** {analysis_data[7]}\n"
                        f"**Force Integrity:** {analysis_data[9]}\n"
                        f"**Control Flow Guard:** {analysis_data[8]}\n"
                        f"**Isolation:** {analysis_data[5]}\n",
            color=0xFB8B00
        )

        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Commands(bot))
