from asyncio import sleep

import discord
from discord.ext import commands

from core import constants
from core.monitoring import (RSS, Google_Alerts, Reddit, Telegram, Twitter,
                             YouTube)


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
    async def addrss(self, context, url):
        rss_class = RSS(bot=None)
        result = await rss_class.add_feed(url)

        if result == False:
            await context.send(f"The URL already exists in the watchlist database, as a result it was not added.")

        elif result == True:
            await context.send(f"Added the URL to the watchlist database.")

    @commands.command()
    async def removerss(self, context, url):
        rss_class = RSS(bot=None)
        result = await rss_class.remove_feed(url)

        if result == False:
            await context.send(f"The URL doesn't exist in the watchlist database, as a result it was not removed.")

        elif result == True:
            await context.send(f"Removed the URL from the watchlist database.")

    @commands.command()
    async def addalert(self, context, url):
        alert_class = Google_Alerts(bot=None)
        result, keyword = await alert_class.add_alert(url)

        if result == False:
            await context.send(f"The alert for `{keyword}` already exists in the watchlist database, as a result it was not added.")

        elif result == True:
            await context.send(f"Added the alert for `{keyword}` to the watchlist database.")

    @commands.command()
    async def removealert(self, context, url):
        alert_class = Google_Alerts(bot=None)
        result, keyword = await alert_class.remove_alert(url)

        if result == False:
            await context.send(f"The alert for `{keyword}` doesn't exist in the watchlist database, as a result it was not removed.")

        elif result == True:
            await context.send(f"Removed the alert for `{keyword}` from the watchlist database.")

    @commands.command()
    async def addsubreddit(self, context, subreddit):
        reddit_class = Reddit(bot=None)
        result = await reddit_class.add_subreddit(subreddit.lower())

        if result == False:
            await context.send(f"`/r/{subreddit.lower()}` already exists in the watchlist database, as a result it was not added.")

        elif result == True:
            await context.send(f"Added `/r/{subreddit.lower()}` to the watchlist database.")

    @commands.command()
    async def removesubreddit(self, context, subreddit):
        reddit_class = Reddit(bot=None)
        result = await reddit_class.remove_subreddit(subreddit.lower())

        if result == False:
            await context.send(f"`/r/{subreddit.lower()}` doesn't exist in the watchlist database, as a result it was not removed.")

        elif result == True:
            await context.send(f"Removed `/r/{subreddit.lower()}` from the watchlist database.")

    @commands.command()
    async def addtelegram(self, context, url):
        telegram_class = Telegram(bot=None)
        result, channel = await telegram_class.add_channel(url)

        if result == False:
            await context.send(f"`{channel}` already exists in the watchlist database, as a result it was not added.")

        elif result == True:
            await context.send(f"Added `{channel}` to the watchlist database.")

    @commands.command()
    async def removetelegram(self, context, url):
        telegram_class = Telegram(bot=None)
        result, channel = await telegram_class.remove_channel(url)

        if result == False:
            await context.send(f"`{channel}` doesn't exist in the watchlist database, as a result it was not removed.")

        elif result == True:
            await context.send(f"Removed `{channel}` from the watchlist database.")

    @commands.command()
    async def addtweeter(self, context, username):
        twitter_class = Twitter(bot=None)
        result = await twitter_class.add_user(username.lower())

        if result == False:
            await context.send(f"`@{username.lower()}` already exists in the watchlist database, as a result it was not added.")

        elif result == True:
            await context.send(f"Added `@{username.lower()}` to the watchlist database.")

    @commands.command()
    async def removetweeter(self, context, username):
        twitter_class = Twitter(bot=None)
        result = await twitter_class.remove_user(username.lower())

        if result == False:
            await context.send(f"`@{username.lower()}` doesn't exist in the watchlist database, as a result it was not removed.")

        elif result == True:
            await context.send(f"Removed `@{username.lower()}` from the watchlist database.")

    @commands.command()
    async def enablerts(self, context, username):
        twitter_class = Twitter(bot=None)
        result = await twitter_class.enable_retweets(username.lower())

        if result == "0":
            await context.send(f"`@{username.lower()}` doesn't exists in the watchlist database, as a result it was not updated.")

        elif result == "1":
            await context.send(f"Retweets from `@{username.lower()}` will now be displayed.")

        elif result == "2":
            await context.send(f"You've already enabled retweets for `@{username.lower()}`. As a result, the value was not updated.")

    @commands.command()
    async def disablerts(self, context, username):
        twitter_class = Twitter(bot=None)
        result = await twitter_class.disable_retweets(username.lower())

        if result == "0":
            await context.send(f"`@{username.lower()}` doesn't exists in the watchlist database, as a result it was not updated.")

        elif result == "1":
            await context.send(f"You've already disabled retweets for `@{username.lower()}`. As a result, the value was not updated.")

        elif result == "2":
            await context.send(f"Retweets from `@{username.lower()}` will now not be displayed.")

    @commands.command()
    async def addchannel(self, context, url):
        youtube_class = YouTube(bot=None)
        result, channel_name = await youtube_class.add_channel(url)

        if result == False:
            await context.send(f"`{channel_name}` already exists in the watchlist database, as a result it was not added.")

        elif result == True:
            await context.send(f"Added `{channel_name}` to the watchlist database.")

    @commands.command()
    async def removechannel(self, context, url):
        youtube_class = YouTube(bot=None)
        result, channel_name = await youtube_class.remove_channel(url)

        if result == False:
            await context.send(f"`{channel_name}` doesn't exist in the watchlist database, as a result it was not removed.")

        elif result == True:
            await context.send(f"Removed `{channel_name}` from the watchlist database.")


def setup(bot):
    bot.add_cog(Commands(bot))
